"""Saved variants: personalize with `save`, ingredient swaps, "I don't have this", consent paths.

Against Postgres with the real catalog and the committed FDC snapshot.
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select, text

from app.core.db import get_sessionmaker
from app.recipes.models import RecipeVariant
from app.variants.models import PlanSlotVariant
from tests.test_auth import FakeApple, apple, apple_key, bearer, client, login
from tests.test_plans import BODY, PROFILE, _create, api, snapshot_catalog
from tests.test_profile import HEALTH, _consent, profile_key

__all__ = ["api", "apple", "apple_key", "client", "profile_key", "snapshot_catalog"]

Json = dict[str, Any]

BOWL = "chicken-rice-broccoli-bowl"
CHICKEN = "0:chicken-breast-raw"
ROLLS = "lazy-cabbage-rolls-buckwheat"
CREAM = "10:sour-cream"
TARGET: Json = {"kcal": 450, "protein_min_g": 45}
FISH_ALLERGY: Json = {"category": "fish", "severity": "allergy"}


async def _recipe_ids(c: AsyncClient) -> dict[str, str]:
    res = await c.get("/v1/recipes", params={"limit": 100})
    return {r["slug"]: r["id"] for r in res.json()["items"]}


async def _personalize(c: AsyncClient, slug: str, body: Json, pair: Json | None = None) -> Any:
    rid = (await _recipe_ids(c))[slug]
    headers = bearer(pair) if pair else {}
    return await c.post(f"/v1/recipes/{rid}/personalize", json=body, headers=headers)


async def _save(c: AsyncClient, pair: Json, slug: str, **save: Any) -> Json:
    res = await _personalize(c, slug, {"target": TARGET, "save": save}, pair)
    assert res.status_code == 200, res.text
    body: Json = res.json()
    assert body["variant_id"]
    return body


async def _variant(c: AsyncClient, pair: Json, variant_id: str) -> Any:
    return await c.get(f"/v1/variants/{variant_id}", headers=bearer(pair))


async def _substitute(c: AsyncClient, pair: Json, variant_id: str, **body: Any) -> Any:
    return await c.post(f"/v1/variants/{variant_id}/substitute", json=body, headers=bearer(pair))


async def _food(c: AsyncClient, slug: str) -> Json:
    body: Json = (await c.get(f"/v1/foods/{slug}")).json()
    return body


# ── personalize and save ────────────────────────────────────────────────────


async def test_personalize_explains_and_stores_nothing_without_save(api: AsyncClient) -> None:
    async with get_sessionmaker()() as session:
        before = await session.scalar(select(func.count()).select_from(RecipeVariant))
    res = await _personalize(api, BOWL, {"target": TARGET})
    assert res.status_code == 200
    body = res.json()
    assert body["variant_id"] is None
    assert body["explanations"]
    assert all(" → " in e["message"] for e in body["explanations"])
    keys = {i["key"] for i in body["ingredients"]}
    assert {e["key"] for e in body["explanations"]} <= keys
    async with get_sessionmaker()() as session:
        assert await session.scalar(select(func.count()).select_from(RecipeVariant)) == before


async def test_save_needs_sign_in(api: AsyncClient) -> None:
    res = await _personalize(api, BOWL, {"target": TARGET, "save": {}})
    assert res.status_code == 401
    bad = {"Authorization": "Bearer nope"}
    rid = (await _recipe_ids(api))[BOWL]
    res = await api.post(f"/v1/recipes/{rid}/personalize", json={"target": TARGET}, headers=bad)
    assert res.status_code == 401


async def test_save_and_read_back(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    proposal = await _save(api, pair, BOWL, label="lighter bowl")
    res = await _variant(api, pair, proposal["variant_id"])
    assert res.status_code == 200
    v = res.json()
    assert v["label"] == "lighter bowl"
    assert v["recipe_id"] == proposal["recipe_id"]
    assert v["target"] == {**TARGET, "fat_g": None, "carbs_g": None}
    assert v["original_nutrition"] == proposal["original_nutrition"]
    assert v["nutrition"]["kcal"] == pytest.approx(proposal["nutrition"]["kcal"], abs=2)
    assert v["on_target"] == proposal["on_target"]
    assert v["explanations"] == proposal["explanations"]
    assert [(x["key"], x["food"]["slug"], x["grams"]) for x in v["lines"]] == [
        (i["key"], i["food"]["slug"], i["grams"]) for i in proposal["ingredients"]
    ]
    assert v["plan_slots"] == []


async def test_variants_are_owner_only(api: AsyncClient, apple: FakeApple) -> None:
    owner = await login(api, apple, "owner")
    other = await login(api, apple, "other")
    vid = (await _save(api, owner, BOWL))["variant_id"]
    assert (await api.get(f"/v1/variants/{vid}")).status_code == 401
    assert (await _variant(api, other, vid)).status_code == 404
    assert (await _variant(api, other, str(uuid.uuid4()))).status_code == 404
    res = await _substitute(api, other, vid, ingredient=CHICKEN)
    assert res.status_code == 404
    assert (await _variant(api, owner, vid)).status_code == 200


async def test_save_into_a_plan_slot(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    plan = await _create(api, pair)
    slot = plan["plan_days"][0]["slots"][1]
    ids = {v: k for k, v in (await _recipe_ids(api)).items()}
    slug = ids[slot["recipe_id"]]
    res = await _personalize(
        api,
        slug,
        {"target": TARGET, "save": {"plan_id": plan["id"], "slot": slot["position"]}},
        pair,
    )
    assert res.status_code == 200, res.text
    vid = res.json()["variant_id"]
    v = (await _variant(api, pair, vid)).json()
    assert v["plan_slots"] == [{"plan_id": plan["id"], "slot": slot["position"]}]

    current = (await api.get("/v1/plans/current", headers=bearer(pair))).json()
    saved = current["plan_days"][0]["slots"][1]
    assert saved["nutrition"]["kcal"] == pytest.approx(
        v["nutrition"]["kcal"] * slot["portion"], abs=2
    )

    # another recipe's slot, someone else's plan, a missing slot
    other_slot = plan["plan_days"][0]["slots"][0]
    if other_slot["recipe_id"] != slot["recipe_id"]:
        body = {"target": TARGET, "save": {"plan_id": plan["id"], "slot": other_slot["position"]}}
        assert (await _personalize(api, slug, body, pair)).status_code == 409
    stranger = await login(api, apple, "stranger")
    body = {"target": TARGET, "save": {"plan_id": plan["id"], "slot": slot["position"]}}
    assert (await _personalize(api, slug, body, stranger)).status_code == 404
    body = {"target": TARGET, "save": {"plan_id": plan["id"], "slot": 999}}
    assert (await _personalize(api, slug, body, pair)).status_code == 404
    body = {"target": TARGET, "save": {"plan_id": plan["id"]}}
    assert (await _personalize(api, slug, body, pair)).status_code == 422


# ── substitute ──────────────────────────────────────────────────────────────


async def test_swap_an_ingredient(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    vid = (await _save(api, pair, BOWL))["variant_id"]
    before = (await _variant(api, pair, vid)).json()
    res = await _substitute(api, pair, vid, ingredient=CHICKEN, food="turkey-breast-raw")
    assert res.status_code == 200, res.text
    out = res.json()
    change = out["change"]
    assert change["kind"] == "swap" and change["key"] == CHICKEN
    assert change["message"].startswith("Swapped Chicken breast")
    assert "to match its protein" in change["message"]
    assert out["previous_nutrition"] == before["nutrition"]
    for k in ("kcal", "protein_g"):
        assert out["delta"][k] == pytest.approx(out["nutrition"][k] - out["previous_nutrition"][k],
                                                abs=1)  # fmt: skip
    line = next(x for x in out["variant"]["lines"] if x["key"] == CHICKEN)
    assert line["food"]["slug"] == "turkey-breast-raw" and line["swapped"]
    assert out["variant"]["explanations"][-1] == change
    assert out["variant"]["nutrition"] == out["nutrition"]
    assert out["conflicts"] == [] and out["rebalance"] == []
    # a same-group swap keeps the protein close
    assert abs(out["delta"]["protein_g"]) < 5

    # the swapped line can be swapped again, and an unknown one is a 404
    res = await _substitute(api, pair, vid, ingredient=CHICKEN, food="chicken-breast-raw")
    assert res.status_code == 200
    assert (await _substitute(api, pair, vid, ingredient="42:nothing")).status_code == 404


async def test_i_dont_have_this(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    vid = (await _save(api, pair, BOWL))["variant_id"]
    out = (await _substitute(api, pair, vid, ingredient=CHICKEN)).json()
    assert out["change"]["message"].startswith("You don't have Chicken breast, raw: using ")
    line = next(x for x in out["variant"]["lines"] if x["key"] == CHICKEN)
    assert line["swapped"] and line["food"]["slug"] != "chicken-breast-raw"

    # an optional ingredient is simply left out
    vid = (await _save(api, pair, ROLLS))["variant_id"]
    out = (await _substitute(api, pair, vid, ingredient=CREAM)).json()
    assert out["change"]["kind"] == "left_out"
    assert out["change"]["message"].startswith("You don't have Sour cream")
    assert out["delta"]["kcal"] < 0
    cream = next(x for x in out["variant"]["lines"] if x["key"] == CREAM)
    assert cream["removed"] and cream["grams"] == 0
    # gone: nothing left to substitute
    assert (await _substitute(api, pair, vid, ingredient=CREAM)).status_code == 404


async def test_substitute_never_introduces_an_excluded_food(
    api: AsyncClient, apple: FakeApple
) -> None:
    pair = await login(api, apple)
    vid = (await _save(api, pair, BOWL))["variant_id"]
    # salmon is a fine swap without exclusions
    res = await _substitute(api, pair, vid, ingredient=CHICKEN, food="salmon-atlantic-raw")
    assert res.status_code == 200, res.text
    vid = (await _save(api, pair, BOWL))["variant_id"]
    res = await _substitute(
        api, pair, vid, ingredient=CHICKEN, food="salmon-atlantic-raw", exclusions=[FISH_ALLERGY]
    )
    assert res.status_code == 422
    for _ in range(3):  # "I don't have this" several times over
        res = await _substitute(api, pair, vid, ingredient=CHICKEN, exclusions=[FISH_ALLERGY])
        assert res.status_code == 200
        line = next(x for x in res.json()["variant"]["lines"] if x["key"] == CHICKEN)
        food = await _food(api, line["food"]["slug"])
        assert "fish" not in food["allergens"] and food["origin"] != "fish"
        # an allergy rules out unknown traces too
        assert food["trace_status"] != "unknown"


async def test_conflicts_left_in_are_reported(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    vid = (await _save(api, pair, BOWL))["variant_id"]
    sesame = {"category": "sesame", "severity": "allergy"}
    out = (await _substitute(api, pair, vid, ingredient=CHICKEN, exclusions=[sesame])).json()
    assert "6:sesame-seeds" in out["conflicts"]
    assert CHICKEN not in out["conflicts"]


async def test_substitute_validation(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    vid = (await _save(api, pair, BOWL))["variant_id"]
    for body in (
        {},
        {"ingredient": "chicken"},
        {"ingredient": CHICKEN, "food": "Not A Slug"},
        {"ingredient": CHICKEN, "exclusions": [{"category": "fish"}]},
        {"ingredient": CHICKEN, "weight_kg": 80},
    ):
        res = await api.post(f"/v1/variants/{vid}/substitute", json=body, headers=bearer(pair))
        assert res.status_code == 422, body
        assert all("input" not in e for e in res.json()["detail"])
    res = await _substitute(api, pair, vid, ingredient=CHICKEN, food="sesame-seeds")
    assert res.status_code == 422  # not a substitute for a main protein


async def test_substitute_updates_the_plan_slots(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    plan = await _create(api, pair)
    ids = {v: k for k, v in (await _recipe_ids(api)).items()}
    slot = plan["plan_days"][0]["slots"][2]
    save = {"plan_id": plan["id"], "slot": slot["position"]}
    proposal = await _save(api, pair, ids[slot["recipe_id"]], **save)
    v = (await _variant(api, pair, proposal["variant_id"])).json()
    line = max(
        (x for x in v["lines"] if not x["removed"] and x["culinary_role"] == "main_protein"),
        key=lambda x: x["grams"],
        default=None,
    )
    if line is None:
        pytest.skip("the planned dinner has no main protein")
    out = (await _substitute(api, pair, v["id"], ingredient=line["key"])).json()
    current = (await api.get("/v1/plans/current", headers=bearer(pair))).json()
    saved = next(s for s in current["plan_days"][0]["slots"] if s["position"] == slot["position"])
    assert saved["nutrition"]["kcal"] == pytest.approx(
        out["nutrition"]["kcal"] * slot["portion"], abs=2
    )
    for proposal in out["rebalance"]:
        assert proposal["plan_id"] == plan["id"] and proposal["day"] == 0
        assert slot["position"] not in {a["slot"] for a in proposal["adjustments"]}


# ── profile: stored with consent, snapshot without ──────────────────────────


async def test_stored_profile_is_used_with_consent(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    await _consent(api, pair, HEALTH)
    salmon = {"category": "other", "severity": "allergy", "term": "salmon"}
    milk = {"category": "milk", "severity": "intolerance"}
    stored = {**PROFILE, "exclusions": [salmon, milk]}
    assert (await api.put("/v1/me/profile", json=stored, headers=bearer(pair))).status_code == 200

    # the body sends no exclusions: the stored intolerance still leaves the cream out
    body = (await _personalize(api, ROLLS, {"target": TARGET}, pair)).json()
    cream = next(i for i in body["ingredients"] if i["key"] == CREAM)
    assert cream["removed"]
    left_out = next(e for e in body["explanations"] if e["key"] == CREAM)
    assert left_out["kind"] == "left_out" and "milk" not in left_out["message"].lower()

    vid = (await _save(api, pair, BOWL))["variant_id"]
    res = await _substitute(api, pair, vid, ingredient=CHICKEN, food="salmon-atlantic-raw")
    assert res.status_code == 422
    # an anonymous request has no stored profile: the same recipe keeps the cream
    anon = (await _personalize(api, ROLLS, {"target": TARGET})).json()
    assert not next(i for i in anon["ingredients"] if i["key"] == CREAM)["removed"]


async def test_snapshot_is_used_and_not_stored_without_consent(
    api: AsyncClient, apple: FakeApple
) -> None:
    pair = await login(api, apple)
    snapshot = [
        {"category": "milk", "severity": "intolerance"},
        {"category": "other", "severity": "dislike", "term": "zzcorianderzz"},
    ]
    res = await _personalize(
        api, ROLLS, {"target": TARGET, "exclusions": snapshot, "save": {}}, pair
    )
    assert res.status_code == 200
    vid = res.json()["variant_id"]
    assert next(i for i in res.json()["ingredients"] if i["key"] == CREAM)["removed"]
    res = await _substitute(api, pair, vid, ingredient="1:buckwheat-groats", exclusions=snapshot)
    assert res.status_code == 200, res.text

    async with get_sessionmaker()() as session:
        stored = " ".join(
            await session.scalars(
                text("SELECT row_to_json(v)::text FROM recipe_variants v WHERE v.id = :id"),
                {"id": vid},
            )
        )
    assert stored
    for word in ("zzcorianderzz", "intolerance", "dislike", "allergy", "exclusion", "milk"):
        assert word not in stored


# ── export and deletion ─────────────────────────────────────────────────────


async def test_export_and_delete(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    keep = await login(api, apple, "keeps-their-data")
    plan = await _create(api, pair, {**BODY, "days": 3})
    ids = {v: k for k, v in (await _recipe_ids(api)).items()}
    slot = plan["plan_days"][1]["slots"][0]
    save = {"label": "mine", "plan_id": plan["id"], "slot": slot["position"]}
    vid = (await _save(api, pair, ids[slot["recipe_id"]], **save))["variant_id"]
    other = (await _save(api, keep, BOWL))["variant_id"]

    export = (await api.get("/v1/me/export", headers=bearer(pair))).json()
    [variant] = [v for v in export["recipe_variants"] if v["id"] == vid]
    assert variant["label"] == "mine"
    assert variant["plan_slots"] == [{"plan_id": plan["id"], "slot": slot["position"]}]
    assert variant["ingredient_changes"] and variant["explanations"] is not None
    assert all(v["id"] != other for v in export["recipe_variants"])

    assert (await api.delete("/v1/me", headers=bearer(pair))).status_code == 204
    async with get_sessionmaker()() as session:
        assert await session.get(RecipeVariant, uuid.UUID(vid)) is None
        links = await session.scalar(select(func.count()).select_from(PlanSlotVariant))
        assert links == 0
        assert await session.get(RecipeVariant, uuid.UUID(other)) is not None
