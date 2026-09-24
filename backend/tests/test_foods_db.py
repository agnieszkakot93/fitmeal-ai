import asyncio
from collections.abc import AsyncIterator
from pathlib import Path

import pytest
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from alembic import command
from app.core.db import get_engine
from app.foods import importer, repository
from app.foods.curated import CuratedFile, load_curated
from app.foods.fdc import load_fdc_dirs
from app.foods.models import FoodAlias, FoodItem
from app.main import app
from app.nutrition.allergens import (
    Allergen,
    Exclusion,
    ExclusionCategory,
    Severity,
    TraceStatus,
    Verdict,
    classify,
)
from tests.conftest import BACKEND_DIR

ROOT = Path(__file__).resolve().parents[2]
CURATED = ROOT / "data" / "foods" / "curated.yaml"
FDC_FIXTURES = Path(__file__).parent / "fixtures" / "fdc"


@pytest.fixture
async def imported(db_session: AsyncSession) -> importer.ImportReport:
    report = importer.resolve(load_curated(CURATED), load_fdc_dirs([FDC_FIXTURES]))
    await importer.apply(db_session, report.resolved)
    await db_session.commit()
    return report


@pytest.fixture
async def client() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


async def test_import_matches_fixture_foods_and_reports_the_rest(
    imported: importer.ImportReport,
) -> None:
    slugs = {r.curated.slug for r in imported.resolved}
    assert slugs == {
        "chicken-breast-raw",
        "egg-whole-raw",
        "olive-oil",
        "milk-skim",
        "rice-white-dry",
    }
    assert "skyr-natural" in imported.pending
    assert "salmon-atlantic-raw" in imported.unmatched


async def test_reimport_is_idempotent(
    db_session: AsyncSession, imported: importer.ImportReport
) -> None:
    before = await db_session.scalar(select(func.count()).select_from(FoodAlias))
    await importer.apply(db_session, imported.resolved)
    await db_session.commit()
    assert await db_session.scalar(select(func.count()).select_from(FoodItem)) == 5
    assert await db_session.scalar(select(func.count()).select_from(FoodAlias)) == before


@pytest.mark.parametrize(
    "query", ["pierś z kurczaka", "piers z kurczaka", "kurcz", "chicken breast"]
)
async def test_search_polish_english_and_prefix(
    imported: importer.ImportReport, client: AsyncClient, query: str
) -> None:
    res = await client.get("/v1/foods/search", params={"q": query})
    assert res.status_code == 200
    assert res.json()[0]["slug"] == "chicken-breast-raw"


async def test_search_lang_filter(imported: importer.ImportReport, client: AsyncClient) -> None:
    res = await client.get("/v1/foods/search", params={"q": "jajko", "lang": "en"})
    assert res.json() == []
    res = await client.get("/v1/foods/search", params={"q": "jajko", "lang": "pl"})
    assert res.json()[0]["slug"] == "egg-whole-raw"


async def test_food_detail(imported: importer.ImportReport, client: AsyncClient) -> None:
    res = await client.get("/v1/foods/egg-whole-raw")
    assert res.status_code == 200
    body = res.json()
    assert body["allergens"] == ["eggs"]
    assert body["may_contain"] == []
    assert body["trace_status"] == "unknown"  # every curated entry is unknown for now
    assert body["portions_g"] == {"piece": 50}
    assert body["source"] == "usda_fdc"
    assert body["source_ref"] == "748967"  # foundation record preferred
    assert "jajko" in body["aliases"]["pl"]

    assert (await client.get("/v1/foods/nope")).status_code == 404


def _label_food(slug: str, **extra: object) -> dict[str, object]:
    return {
        "slug": slug,
        "name": {"en": slug.title(), "pl": slug},
        "category": "sweets_baking",
        "origin": "plant",
        "culinary_roles": ["sweetener"],
        "nutrition": {
            "kcal": 500,
            "protein_g": 5,
            "fat_g": 30,
            "carbs_g": 50,
            "fiber_g": 5,
            "source_ref": "test label",
        },
        **extra,
    }


def _declared(ref: str) -> dict[str, object]:
    return {"status": "declared", "source": {"type": "label", "ref": ref}}


NONE_DECLARED = {"status": "none_declared", "source": {"type": "label", "ref": "sugar pack"}}


@pytest.fixture
async def traced(db_session: AsyncSession) -> None:
    curated = CuratedFile.model_validate(
        {
            "foods": [
                _label_food(
                    "chocolate",
                    allergens=["milk"],
                    may_contain=["peanuts"],
                    traces=_declared("choc pack"),
                ),
                # its "milk" trace is dropped: it inherits "contains milk"
                _label_food(
                    "choc-bar",
                    derived_from=["chocolate"],
                    may_contain=["milk", "sesame"],
                    traces=_declared("bar pack"),
                ),
                _label_food("sugar", traces=NONE_DECLARED),
                # traces unknown, and so is everything made from it
                _label_food("cocoa"),
                _label_food("cocoa-bar", derived_from=["cocoa", "sugar"], traces=NONE_DECLARED),
                _label_food(
                    "verified-sugar",
                    traces=NONE_DECLARED,
                    review={"status": "verified", "by": "AK", "date": "2026-09-24"},
                ),
            ]
        }
    )
    report = importer.resolve(curated, None)
    await importer.apply(db_session, report.resolved)
    await db_session.commit()


async def test_may_contain_round_trips_through_the_db(
    db_session: AsyncSession, traced: None
) -> None:
    items = await repository.get_by_slugs(db_session, ["chocolate", "choc-bar", "sugar"])
    assert items["chocolate"].may_contain == ["peanuts"]
    assert items["chocolate"].effective_may_contain == ["peanuts"]
    assert items["choc-bar"].may_contain == ["milk", "sesame"]
    assert items["choc-bar"].effective_may_contain == ["peanuts", "sesame"]
    assert items["choc-bar"].effective_allergens == ["milk"]
    assert items["sugar"].may_contain == []
    assert items["sugar"].effective_may_contain == []


async def test_trace_status_and_review_reach_the_db(db_session: AsyncSession, traced: None) -> None:
    items = await repository.get_by_slugs(
        db_session, ["chocolate", "choc-bar", "sugar", "cocoa", "cocoa-bar", "verified-sugar"]
    )
    own = {slug: item.trace_status for slug, item in items.items()}
    effective = {slug: item.effective_trace_status for slug, item in items.items()}
    assert own == {
        "chocolate": "declared",
        "choc-bar": "declared",
        "sugar": "none_declared",
        "cocoa": "unknown",
        "cocoa-bar": "none_declared",
        "verified-sugar": "none_declared",
    }
    assert effective == {**own, "cocoa-bar": "unknown"}
    assert {slug for slug, item in items.items() if item.reviewed} == {"verified-sugar"}


async def test_unknown_trace_status_reaches_the_exclusion_check(
    db_session: AsyncSession, traced: None
) -> None:
    items = await repository.get_by_slugs(db_session, ["sugar", "cocoa-bar"])
    sugar, cocoa_bar = (repository.to_allergens(items[s]) for s in ("sugar", "cocoa-bar"))
    assert sugar.trace_status is TraceStatus.NONE_DECLARED
    assert cocoa_bar.trace_status is TraceStatus.UNKNOWN
    sesame_allergy = Exclusion(ExclusionCategory.SESAME, Severity.ALLERGY)
    assert classify(sugar, sesame_allergy) is Verdict.ALLOWED
    assert classify(cocoa_bar, sesame_allergy) is Verdict.EXCLUDED
    sesame_intolerance = Exclusion(ExclusionCategory.SESAME, Severity.INTOLERANCE)
    assert classify(cocoa_bar, sesame_intolerance) is Verdict.ALLOWED


async def test_stored_traces_reach_the_exclusion_check(
    db_session: AsyncSession, traced: None
) -> None:
    bar = await repository.get_by_slug(db_session, "choc-bar")
    assert bar is not None
    food = repository.to_allergens(bar)
    assert food.contains == {Allergen.MILK}
    assert food.may_contain == {Allergen.PEANUTS, Allergen.SESAME}
    assert "Choc-Bar" in food.names
    peanuts = ExclusionCategory.PEANUTS
    assert classify(food, Exclusion(peanuts, Severity.ALLERGY)) is Verdict.EXCLUDED
    assert classify(food, Exclusion(peanuts, Severity.INTOLERANCE)) is Verdict.ALLOWED


async def test_food_detail_reports_traces(traced: None, client: AsyncClient) -> None:
    body = (await client.get("/v1/foods/choc-bar")).json()
    assert body["allergens"] == ["milk"]
    assert body["may_contain"] == ["peanuts", "sesame"]
    assert body["trace_status"] == "declared"
    sugar = (await client.get("/v1/foods/sugar")).json()
    assert sugar["may_contain"] == []
    assert sugar["trace_status"] == "none_declared"
    # inherited: its own label declares none, but cocoa is unknown
    assert (await client.get("/v1/foods/cocoa-bar")).json()["trace_status"] == "unknown"


async def test_openapi_documents_may_contain(client: AsyncClient) -> None:
    detail = (await client.get("/openapi.json")).json()["components"]["schemas"]["FoodDetail"]
    assert "may_contain" in detail["required"]
    assert detail["properties"]["may_contain"]["type"] == "array"


async def test_openapi_documents_trace_status(client: AsyncClient) -> None:
    schemas = (await client.get("/openapi.json")).json()["components"]["schemas"]
    detail = schemas["FoodDetail"]
    assert "trace_status" in detail["required"]
    assert detail["properties"]["trace_status"]["$ref"] == "#/components/schemas/TraceStatus"
    assert schemas["TraceStatus"]["enum"] == ["unknown", "none_declared", "declared"]


# ── Migration 0003 ──────────────────────────────────────────────────────────


async def _alembic(action: str, revision: str) -> None:
    # env.py runs its own event loop, so alembic gets a thread of its own
    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    await asyncio.to_thread(getattr(command, action), cfg, revision)


async def _columns(session: AsyncSession) -> set[str]:
    rows = await session.scalars(
        text("SELECT column_name FROM information_schema.columns WHERE table_name = 'food_items'")
    )
    return set(rows)


@pytest.fixture
async def at_0002(db_session: AsyncSession) -> AsyncIterator[AsyncSession]:
    await db_session.commit()  # release any lock before alembic alters the table
    await _alembic("downgrade", "0002")
    try:
        yield db_session
    finally:
        await db_session.rollback()
        await _alembic("upgrade", "head")
        # drop pooled connections whose cached statements saw the old table
        await get_engine().dispose()


async def test_migration_0003_round_trip(at_0002: AsyncSession) -> None:
    session = at_0002
    assert not {"trace_status", "effective_trace_status"} & await _columns(session)
    await session.execute(
        text(
            "INSERT INTO food_items (slug, name_en, name_pl, category, origin, kcal, protein_g,"
            " fat_g, carbs_g, fiber_g, source) VALUES"
            " ('old', 'Old', 'Stare', 'other', 'plant', 1, 0, 0, 0, 0, 'label')"
        )
    )
    await session.commit()

    await _alembic("upgrade", "0003")
    row = (
        await session.execute(
            text("SELECT trace_status, effective_trace_status FROM food_items WHERE slug = 'old'")
        )
    ).one()
    assert tuple(row) == ("unknown", "unknown")  # existing foods are never "none"
    await session.commit()
    with pytest.raises(IntegrityError):
        await session.execute(text("UPDATE food_items SET trace_status = 'none'"))
    await session.rollback()

    await _alembic("downgrade", "0002")
    assert not {"trace_status", "effective_trace_status"} & await _columns(session)
    await session.commit()


async def test_calculate_recipe_nutrition(
    imported: importer.ImportReport, client: AsyncClient
) -> None:
    res = await client.post(
        "/v1/nutrition/calculate",
        json={
            "servings": 2,
            "ingredients": [
                {"food": "chicken-breast-raw", "amount": 400, "unit": "g"},
                {"food": "olive-oil", "amount": 1, "unit": "łyżka"},
                {"food": "egg-whole-raw", "amount": 2, "unit": "szt"},
            ],
        },
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert [line["grams"] for line in body["lines"]] == [400, 13.7, 100]
    # 480 (chicken) + 120.7 (13.65 g oil) + 148 (2 foundation eggs)
    assert body["total"]["kcal"] == 749
    assert body["per_serving"]["kcal"] == 374


async def test_calculate_reports_every_unresolvable_line(
    imported: importer.ImportReport, client: AsyncClient
) -> None:
    res = await client.post(
        "/v1/nutrition/calculate",
        json={
            "ingredients": [
                {"food": "chicken-breast-raw", "amount": 1, "unit": "cup"},
                {"food": "olive-oil", "amount": 1, "unit": "tbsp"},
                {"food": "egg-whole-raw", "amount": 1, "unit": "scoop"},
            ]
        },
    )
    assert res.status_code == 422
    assert [e["index"] for e in res.json()["detail"]] == [0, 2]


async def test_healthz(migrated_db: None, client: AsyncClient) -> None:
    res = await client.get("/healthz")
    assert res.json() == {"status": "ok"}
