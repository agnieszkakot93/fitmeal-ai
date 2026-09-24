from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.foods import importer
from app.foods.curated import load_curated
from app.foods.fdc import load_fdc_dirs
from app.foods.models import FoodAlias, FoodItem
from app.main import app

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
    assert body["portions_g"] == {"piece": 50}
    assert body["source"] == "usda_fdc"
    assert body["source_ref"] == "748967"  # foundation record preferred
    assert "jajko" in body["aliases"]["pl"]

    assert (await client.get("/v1/foods/nope")).status_code == 404


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
