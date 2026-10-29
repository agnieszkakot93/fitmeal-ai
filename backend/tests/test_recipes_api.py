"""Recipes API against Postgres with the real catalog and the committed FDC snapshot."""

import uuid
from collections.abc import AsyncIterator
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete, text, update

from app.core.db import get_sessionmaker
from app.foods import importer
from app.foods.curated import load_curated
from app.foods.fdc import load_fdc_dirs
from app.main import app
from app.recipes import catalog
from app.recipes.models import Recipe
from app.users.models import User
from tests.test_foods_db import CURATED
from tests.test_tuning import CATALOG, SNAPSHOT

Json = dict[str, Any]


@pytest.fixture(scope="module")
async def loaded(migrated_db: None) -> None:
    """Foods and catalog loaded once; the tests here only read."""
    async with get_sessionmaker()() as session:
        await session.execute(text("TRUNCATE food_items, recipe_sources CASCADE"))
        report = importer.resolve(load_curated(CURATED), load_fdc_dirs([SNAPSHOT]))
        await importer.apply(session, report.resolved)
        written = await catalog.apply(session, catalog.load_catalog(CATALOG))
        await session.commit()
    assert len(written.written) == 60


@pytest.fixture
async def client(loaded: None) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


async def _by_slug(client: AsyncClient) -> dict[str, Json]:
    res = await client.get("/v1/recipes", params={"limit": 100})
    assert res.status_code == 200
    return {r["slug"]: r for r in res.json()["items"]}


async def _id(client: AsyncClient, slug: str) -> str:
    return str((await _by_slug(client))[slug]["id"])


async def _detail(client: AsyncClient, slug: str) -> Json:
    res = await client.get(f"/v1/recipes/{await _id(client, slug)}")
    assert res.status_code == 200
    body: Json = res.json()
    return body


# ── list and search ─────────────────────────────────────────────────────────


async def test_list_returns_the_catalog_with_per_serving_nutrition(client: AsyncClient) -> None:
    res = await client.get("/v1/recipes", params={"limit": 100})
    body = res.json()
    assert body["total"] == 60
    assert len(body["items"]) == 60
    oatmeal = next(r for r in body["items"] if r["slug"] == "protein-oatmeal-berries")
    assert oatmeal["total_minutes"] == 8
    assert oatmeal["per_serving"]["kcal"] > 0
    assert oatmeal["allergens"] == ["gluten", "milk"]
    assert oatmeal["conflicts"] == []


async def test_list_pages(client: AsyncClient) -> None:
    everything = (await client.get("/v1/recipes", params={"limit": 100})).json()["items"]
    page = (await client.get("/v1/recipes", params={"limit": 10, "offset": 10})).json()
    assert page["total"] == 60
    assert [r["id"] for r in page["items"]] == [r["id"] for r in everything[10:20]]


async def test_tag_filter_needs_every_tag(client: AsyncClient) -> None:
    everything = (await _by_slug(client)).values()
    expected = {r["slug"] for r in everything if {"vegan", "dinner"} <= set(r["tags"])}
    res = await client.get("/v1/recipes", params=[("tag", "vegan"), ("tag", "dinner")])
    found = {r["slug"] for r in res.json()["items"]}
    assert found == expected
    assert 0 < len(found) < 12


async def test_max_total_minutes(client: AsyncClient) -> None:
    res = await client.get("/v1/recipes", params={"max_total_minutes": 15, "limit": 100})
    items = res.json()["items"]
    assert items
    assert all(r["total_minutes"] <= 15 for r in items)
    assert res.json()["total"] < 60


@pytest.mark.parametrize(
    "params",
    [{"max_total_minutes": 0}, {"limit": 500}, {"offset": -1}, {"max_total_minutes": "soon"}],
)
async def test_list_validation(client: AsyncClient, params: dict[str, int | str]) -> None:
    assert (await client.get("/v1/recipes", params=params)).status_code == 422


async def test_allergy_exclusion_hides_blocked_recipes(client: AsyncClient) -> None:
    res = await client.post(
        "/v1/recipes/search",
        json={"exclusions": [{"category": "milk", "severity": "allergy"}], "limit": 100},
    )
    assert res.status_code == 200
    body = res.json()
    slugs = {r["slug"] for r in body["items"]}
    assert "protein-oatmeal-berries" not in slugs  # skim milk and whey
    assert 0 < body["total"] < 60
    for recipe in body["items"]:
        # whatever is still listed only conflicts in optional ingredients
        excluded = [c for c in recipe["conflicts"] if c["verdict"] == "excluded"]
        assert all(c["optional"] for c in excluded)
        if "milk" in recipe["allergens"]:
            assert excluded


async def test_dislike_ranks_but_hides_nothing(client: AsyncClient) -> None:
    res = await client.post(
        "/v1/recipes/search",
        json={"exclusions": [{"category": "meat", "severity": "dislike"}], "limit": 100},
    )
    body = res.json()
    assert body["total"] == 60
    bowl = next(r for r in body["items"] if r["slug"] == "chicken-rice-broccoli-bowl")
    assert {"key": "0:chicken-breast-raw", "verdict": "penalised", "optional": False} in bowl[
        "conflicts"
    ]


async def test_search_combines_filters_and_exclusions(client: AsyncClient) -> None:
    res = await client.post(
        "/v1/recipes/search",
        json={
            "tags": ["breakfast"],
            "max_total_minutes": 20,
            "exclusions": [{"category": "eggs", "severity": "intolerance"}],
            "limit": 100,
        },
    )
    items = res.json()["items"]
    assert items
    slugs = {r["slug"] for r in items}
    assert "veggie-scrambled-eggs" not in slugs
    assert all("breakfast" in r["tags"] and r["total_minutes"] <= 20 for r in items)


@pytest.mark.parametrize(
    "exclusion",
    [
        {"category": "other", "severity": "allergy"},  # other needs a term
        {"category": "other", "severity": "allergy", "term": "   "},
        {"category": "milk", "severity": "allergy", "term": "CANARY-7f3a"},  # term only for other
        {"category": "milk", "severity": "allergy", "relaxed": True},  # allergies can't relax
        {"category": "chocolate", "severity": "allergy"},
        {"category": "milk", "severity": "hate"},
        {"category": "milk", "severity": "allergy", "note": "CANARY-7f3a"},  # extra field
    ],
)
async def test_invalid_exclusions_are_rejected_without_echoing_input(
    client: AsyncClient, exclusion: Json
) -> None:
    res = await client.post("/v1/recipes/search", json={"exclusions": [exclusion]})
    assert res.status_code == 422
    assert "CANARY" not in res.text
    assert all("input" not in e for e in res.json()["detail"])


async def test_too_many_exclusions(client: AsyncClient) -> None:
    exclusions = [{"category": "other", "severity": "dislike", "term": f"x{i}"} for i in range(41)]
    res = await client.post("/v1/recipes/search", json={"exclusions": exclusions})
    assert res.status_code == 422


# ── detail ──────────────────────────────────────────────────────────────────


async def test_detail_has_ingredients_nutrition_and_allergens(client: AsyncClient) -> None:
    summary = (await _by_slug(client))["overnight-oats-apple-cinnamon"]
    detail = await _detail(client, "overnight-oats-apple-cinnamon")
    assert detail["title_en"] == "Apple cinnamon overnight oats"
    assert [i["key"] for i in detail["ingredients"]][:2] == [
        "0:oats-rolled",
        "1:greek-yogurt-nonfat",
    ]
    walnuts = next(i for i in detail["ingredients"] if i["food"]["slug"] == "walnuts")
    assert walnuts["allergens"] == ["tree_nuts"]
    assert walnuts["per_serving_g"] == walnuts["amount_g"]  # one serving
    assert set(detail["allergens"]) == {"gluten", "milk", "tree_nuts"}
    assert detail["nutrition"]["per_serving"] == summary["per_serving"]
    assert detail["instructions_pl"]
    assert detail["fridge_days"] == 3


async def test_unknown_recipe_is_404(client: AsyncClient) -> None:
    missing = uuid.uuid4()
    assert (await client.get(f"/v1/recipes/{missing}")).status_code == 404
    res = await client.post(
        f"/v1/recipes/{missing}/personalize", json={"target": {"kcal": 500, "protein_min_g": 30}}
    )
    assert res.status_code == 404
    res = await client.get(f"/v1/recipes/{missing}/substitutions", params={"ingredient": 0})
    assert res.status_code == 404


async def test_bad_recipe_id_is_422(client: AsyncClient) -> None:
    assert (await client.get("/v1/recipes/not-a-uuid")).status_code == 422


async def test_private_recipes_are_not_served(client: AsyncClient) -> None:
    recipe_id = uuid.UUID(await _id(client, "banana-bread-oat"))
    owner = User(apple_sub=f"test-{uuid.uuid4()}")
    async with get_sessionmaker()() as session:
        session.add(owner)
        await session.flush()
        await session.execute(
            update(Recipe).where(Recipe.id == recipe_id).values(owner_user_id=owner.id)
        )
        await session.commit()
    try:
        assert (await client.get(f"/v1/recipes/{recipe_id}")).status_code == 404
        assert "banana-bread-oat" not in await _by_slug(client)
    finally:
        async with get_sessionmaker()() as session:
            await session.execute(
                update(Recipe).where(Recipe.id == recipe_id).values(owner_user_id=None)
            )
            await session.execute(delete(User).where(User.id == owner.id))
            await session.commit()


# ── personalize ─────────────────────────────────────────────────────────────


async def _personalize(client: AsyncClient, slug: str, body: Json) -> Any:
    return await client.post(f"/v1/recipes/{await _id(client, slug)}/personalize", json=body)


async def test_personalize_hits_the_target(client: AsyncClient) -> None:
    per_serving = (await _by_slug(client))["protein-oatmeal-berries"]["per_serving"]
    kcal, protein = per_serving["kcal"] * 0.85, per_serving["protein_g"] * 1.1
    res = await _personalize(
        client,
        "protein-oatmeal-berries",
        {"target": {"kcal": kcal, "protein_min_g": protein}},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["on_target"] is True
    assert body["misses"] == []
    assert abs(body["nutrition"]["kcal"] - kcal) <= 0.05 * kcal
    assert body["nutrition"]["protein_g"] >= protein - 0.1
    assert body["original_nutrition"] == per_serving
    assert body["changes"]
    assert all(c["reason"] for c in body["changes"])
    assert [i["position"] for i in body["ingredients"]] == list(range(6))
    for swap in body["swaps"]:
        proposed = next(i for i in body["ingredients"] if i["key"] == swap["original_key"])
        assert proposed["swapped"] and proposed["food"] == swap["food"]


async def test_personalize_reports_an_unreachable_target(client: AsyncClient) -> None:
    res = await _personalize(
        client, "cottage-cheese-berries-snack", {"target": {"kcal": 2500, "protein_min_g": 10}}
    )
    body = res.json()
    assert body["on_target"] is False
    assert [m["metric"] for m in body["misses"]] == ["kcal"]
    assert body["misses"][0]["target"] == 2500


async def test_personalize_blocks_an_excluded_required_ingredient(client: AsyncClient) -> None:
    res = await _personalize(
        client,
        "overnight-oats-apple-cinnamon",
        {
            "target": {"kcal": 450, "protein_min_g": 25},
            "exclusions": [{"category": "nuts", "severity": "intolerance"}],
        },
    )
    assert res.status_code == 409
    assert res.json()["detail"]["must_substitute"] == ["5:walnuts"]


async def test_personalize_leaves_out_an_excluded_optional_ingredient(
    client: AsyncClient,
) -> None:
    res = await _personalize(
        client,
        "lazy-cabbage-rolls-buckwheat",
        {
            "target": {"kcal": 450, "protein_min_g": 25},
            "exclusions": [{"category": "milk", "severity": "intolerance"}],
        },
    )
    assert res.status_code == 200
    body = res.json()
    cream = next(i for i in body["ingredients"] if i["original_food"] == "sour-cream")
    assert cream["removed"] is True
    assert cream["grams"] == 0
    assert {"key": cream["key"], "original_g": cream["original_g"], "grams": 0,
            "reason": "excluded"} in body["changes"]  # fmt: skip
    for ingredient in body["ingredients"]:
        if ingredient["removed"]:
            continue
        food = (await client.get(f"/v1/foods/{ingredient['food']['slug']}")).json()
        assert "milk" not in food["allergens"]


async def test_personalize_swaps_respect_exclusions(client: AsyncClient) -> None:
    per_serving = (await _by_slug(client))["protein-oatmeal-berries"]["per_serving"]
    target = {"kcal": per_serving["kcal"] * 0.85, "protein_min_g": per_serving["protein_g"] * 1.1}
    plain = (await _personalize(client, "protein-oatmeal-berries", {"target": target})).json()
    assert [s["food"]["slug"] for s in plain["swaps"]] == ["oat-bran"]

    res = await _personalize(
        client,
        "protein-oatmeal-berries",
        {
            "target": target,
            "exclusions": [{"category": "other", "severity": "intolerance", "term": "bran"}],
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert all(s["food"]["slug"] != "oat-bran" for s in body["swaps"])
    assert all(i["food"]["slug"] != "oat-bran" for i in body["ingredients"])


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"target": {"kcal": 0, "protein_min_g": 30}},
        {"target": {"kcal": 50000, "protein_min_g": 30}},
        {"target": {"kcal": 500, "protein_min_g": -1}},
        {"target": {"kcal": 500}},
        {"target": {"kcal": 500, "protein_min_g": 30, "fat_g": 1000}},
        {"target": {"kcal": 500, "protein_min_g": 30, "weight_kg": 80}},
        {"target": {"kcal": 500, "protein_min_g": 30}, "exclusions": [{"category": "milk"}]},
    ],
)
async def test_personalize_validation(client: AsyncClient, body: Json) -> None:
    res = await _personalize(client, "protein-oatmeal-berries", body)
    assert res.status_code == 422
    assert all("input" not in e for e in res.json()["detail"])


# ── substitutions ───────────────────────────────────────────────────────────


async def _substitutions(client: AsyncClient, slug: str, body: Json) -> Json:
    res = await client.post(f"/v1/recipes/{await _id(client, slug)}/substitutions", json=body)
    assert res.status_code == 200
    out: Json = res.json()
    return out


async def test_substitutions_rank_options_with_deltas(client: AsyncClient) -> None:
    recipe_id = await _id(client, "chicken-rice-broccoli-bowl")
    res = await client.get(f"/v1/recipes/{recipe_id}/substitutions", params={"ingredient": 0})
    assert res.status_code == 200
    body = res.json()
    assert body["key"] == "0:chicken-breast-raw"
    assert body["culinary_role"] == "main_protein"
    assert body["excluded"] is False
    options = body["options"]
    assert 0 < len(options) <= 5
    assert [o["score"] for o in options] == sorted(o["score"] for o in options)
    assert all(set(o["delta"]) == {"kcal", "protein_g", "fat_g", "carbs_g", "fiber_g"}
               for o in options)  # fmt: skip
    # main protein swaps keep the protein
    assert all(abs(o["delta"]["protein_g"]) < 5 for o in options if o["grams"] < 300)


async def test_substitutions_never_offer_an_allergen(client: AsyncClient) -> None:
    body = await _substitutions(
        client,
        "chicken-rice-broccoli-bowl",
        {"ingredient": 0, "exclusions": [{"category": "fish", "severity": "allergy"}], "limit": 20},
    )
    assert body["options"]
    for option in body["options"]:
        food = (await client.get(f"/v1/foods/{option['food']['slug']}")).json()
        assert "fish" not in food["allergens"] and food["origin"] != "fish"
        assert food["trace_status"] != "unknown"


async def test_substitutions_rank_dislikes_down(client: AsyncClient) -> None:
    plain = await _substitutions(client, "chicken-rice-broccoli-bowl", {"ingredient": 0})
    assert plain["options"][0]["food"]["slug"] == "turkey-breast-raw"
    body = await _substitutions(
        client,
        "chicken-rice-broccoli-bowl",
        {"ingredient": 0, "exclusions": [{"category": "meat", "severity": "dislike"}], "limit": 20},
    )
    # turkey is still allowed, but ranks below every food the user doesn't mind
    ranked = [(o["food"]["slug"], o["disliked"]) for o in body["options"]]
    assert ranked[0] != ("turkey-breast-raw", False)
    assert [d for _, d in ranked] == sorted(d for _, d in ranked)
    assert all(d for slug, d in ranked if slug.startswith(("turkey", "chicken", "pork")))


async def test_substitutions_for_an_excluded_ingredient(client: AsyncClient) -> None:
    body = await _substitutions(
        client,
        "overnight-oats-apple-cinnamon",
        {"ingredient": 5, "exclusions": [{"category": "nuts", "severity": "intolerance"}]},
    )
    assert body["key"] == "5:walnuts"
    assert body["excluded"] is True
    assert body["remove"] is False
    for option in body["options"]:
        food = (await client.get(f"/v1/foods/{option['food']['slug']}")).json()
        assert not {"tree_nuts", "peanuts"} & set(food["allergens"])


async def test_substitutions_suggest_removing_an_excluded_optional(client: AsyncClient) -> None:
    detail = await _detail(client, "lazy-cabbage-rolls-buckwheat")
    cream = next(i for i in detail["ingredients"] if i["food"]["slug"] == "sour-cream")
    body = await _substitutions(
        client,
        "lazy-cabbage-rolls-buckwheat",
        {
            "ingredient": cream["position"],
            "exclusions": [{"category": "milk", "severity": "intolerance"}],
        },
    )
    assert body["excluded"] is True
    assert body["remove"] is True
    assert body["options"] == []


async def test_substitutions_validation_and_404(client: AsyncClient) -> None:
    recipe_id = await _id(client, "chicken-rice-broccoli-bowl")
    url = f"/v1/recipes/{recipe_id}/substitutions"
    assert (await client.get(url)).status_code == 422  # ingredient is required
    assert (await client.get(url, params={"ingredient": -1})).status_code == 422
    assert (await client.get(url, params={"ingredient": 0, "limit": 99})).status_code == 422
    res = await client.get(url, params={"ingredient": 99})
    assert res.status_code == 404
    assert res.json()["detail"] == "ingredient not found"
    assert (await client.post(url, json={"exclusions": []})).status_code == 422
