"""Plans API against Postgres, on the real catalog and the committed FDC snapshot."""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select, text

from app.core.db import get_sessionmaker
from app.foods import importer
from app.foods.curated import load_curated
from app.foods.fdc import load_fdc_dirs
from app.plans.models import MealPlan, SlotEvent
from app.recipes import catalog
from tests.test_auth import FakeApple, apple, apple_key, bearer, client, login
from tests.test_foods_db import CURATED
from tests.test_planner_catalog import CATALOG, SNAPSHOT

__all__ = ["apple", "apple_key", "client"]  # fixtures shared with test_auth

Json = dict[str, Any]

PROFILE: Json = {
    "daily_kcal": 2000,
    "protein_min_g": 120,
    "meals": [
        {"name": "breakfast", "meal_type": "breakfast", "kcal_share": 0.3},
        {"name": "lunch", "meal_type": "lunch", "kcal_share": 0.35},
        {"name": "dinner", "meal_type": "dinner", "kcal_share": 0.35},
    ],
    "max_minutes": 60,
    "equipment": ["oven", "blender"],
}
BODY: Json = {"days": 3, "prep_days": 2, "profile": PROFILE}


@pytest.fixture(scope="module")
async def snapshot_catalog(migrated_db: None) -> AsyncIterator[None]:
    async with get_sessionmaker()() as session:
        await session.execute(text("TRUNCATE food_items, recipe_sources CASCADE"))
        report = importer.resolve(load_curated(CURATED), load_fdc_dirs([SNAPSHOT]))
        await importer.apply(session, report.resolved)
        written = await catalog.apply(session, catalog.load_catalog(CATALOG))
        assert written.written and not written.skipped, written.summary()
        await session.commit()
    yield


@pytest.fixture
async def api(snapshot_catalog: None, client: AsyncClient) -> AsyncClient:
    return client


async def _create(c: AsyncClient, pair: Json, body: Json = BODY) -> Json:
    res = await c.post("/v1/plans", json=body, headers=bearer(pair))
    assert res.status_code == 201, res.text
    plan: Json = res.json()
    return plan


async def _patch(c: AsyncClient, pair: Json, plan: Json, slot: int, **body: Any) -> Any:
    return await c.patch(f"/v1/plans/{plan['id']}/slots/{slot}", json=body, headers=bearer(pair))


async def _count(model: type[MealPlan] | type[SlotEvent]) -> int:
    async with get_sessionmaker()() as session:
        return int(await session.scalar(select(func.count()).select_from(model)) or 0)


async def test_auth_required(api: AsyncClient) -> None:
    assert (await api.post("/v1/plans", json=BODY)).status_code == 401
    assert (await api.get("/v1/plans/current")).status_code == 401
    res = await api.patch(
        f"/v1/plans/{uuid.uuid4()}/slots/0", json={"status": "eaten", "event_id": str(uuid.uuid4())}
    )
    assert res.status_code == 401


async def test_generate_from_the_snapshot_catalog(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    plan = await _create(api, pair)

    assert plan["days"] == 3 and plan["prep_days"] == 2
    assert plan["targets"] == {"daily_kcal": 2000, "protein_min_g": 120}
    assert [d["day"] for d in plan["plan_days"]] == [0, 1, 2]
    positions = []
    for day in plan["plan_days"]:
        assert [s["slot"] for s in day["slots"]] == ["breakfast", "lunch", "dinner"]
        # ±5% of the target, protein at the minimum (rounding aside)
        assert 1900 - 1 <= day["totals"]["kcal"] <= 2100 + 1
        assert day["totals"]["protein_g"] >= 120 - 0.5
        for s in day["slots"]:
            positions.append(s["position"])
            assert s["recipe_slug"] and s["recipe_id"]
            assert s["status"] == "planned"
            assert 0.5 <= s["portion"] <= 2.0
    assert positions == list(range(9))
    # cook once for 2 days: some meals come from a batch
    assert any(s["from_batch"] for d in plan["plan_days"] for s in d["slots"])

    current = await api.get("/v1/plans/current", headers=bearer(pair))
    assert current.status_code == 200
    assert current.json() == plan


async def test_newest_plan_is_current(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    assert (await api.get("/v1/plans/current", headers=bearer(pair))).status_code == 404
    await _create(api, pair)
    second = await _create(api, pair, {**BODY, "days": 5})
    current = (await api.get("/v1/plans/current", headers=bearer(pair))).json()
    assert current["id"] == second["id"] and len(current["plan_days"]) == 5


async def test_profile_is_not_stored(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    # a soft exclusion the catalog can't fully avoid, so the plan carries labels
    exclusions = [{"category": "milk", "severity": "prefer_not"}]
    plan = await _create(api, pair, {**BODY, "profile": {**PROFILE, "exclusions": exclusions}})
    # labels come from the exclusions: shown once, never saved
    labels = [label for d in plan["plan_days"] for s in d["slots"] for label in s["labels"]]
    assert labels and all("prefer not" in label for label in labels)
    current = (await api.get("/v1/plans/current", headers=bearer(pair))).json()
    assert all(s["labels"] == [] for d in current["plan_days"] for s in d["slots"])

    async with get_sessionmaker()() as session:
        rows = await session.scalars(
            text(
                "SELECT row_to_json(p)::text FROM plans p UNION ALL "
                "SELECT row_to_json(s)::text FROM plan_slots s"
            )
        )
        stored = " ".join(rows)
    for word in ("prefer", "milk", "oven", "blender", "exclusion"):
        assert word not in stored


async def test_infeasible_gets_the_report(api: AsyncClient, apple: FakeApple) -> None:
    # most catalog foods have unknown traces, and a milk allergy excludes those
    pair = await login(api, apple)
    exclusions = [{"category": "milk", "severity": "allergy"}]
    body = {**BODY, "profile": {**PROFILE, "exclusions": exclusions}}
    res = await api.post("/v1/plans", json=body, headers=bearer(pair))
    assert res.status_code == 422
    report = res.json()
    assert report["status"] == "infeasible"
    assert report["blockers"] and all("milk" in b["message"] for b in report["blockers"])
    assert {s["action"] for s in report["suggestions"]} == {"add_recipes"}
    assert report["message"].startswith(report["blockers"][0]["message"])
    assert await _count(MealPlan) == 0


@pytest.mark.parametrize(
    "change",
    [
        {"days": 4},
        {"prep_days": 4},
        {"profile": {**PROFILE, "daily_kcal": 1100}},
        {"profile": {**PROFILE, "meals": PROFILE["meals"][:1]}},
        {"profile": {**PROFILE, "meals": [{**m, "kcal_share": 0.2} for m in PROFILE["meals"]]}},
        {"profile": {**PROFILE, "exclusions": [{"category": "milk", "severity": "x"}]}},
        {"profile": {**PROFILE, "weight_kg": 80}},
    ],
)
async def test_invalid_body_is_rejected_without_echo(
    api: AsyncClient, apple: FakeApple, change: Json
) -> None:
    pair = await login(api, apple)
    res = await api.post("/v1/plans", json={**BODY, **change}, headers=bearer(pair))
    assert res.status_code == 422
    for error in res.json()["detail"]:
        assert "input" not in error


async def test_slot_status_replay_is_idempotent(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    plan = await _create(api, pair)
    eaten, skipped = str(uuid.uuid4()), str(uuid.uuid4())

    res = await _patch(api, pair, plan, 1, status="eaten", event_id=eaten)
    assert res.status_code == 200, res.text
    assert res.json()["status"] == "eaten" and res.json()["position"] == 1
    first_at = res.json()["status_updated_at"]
    assert first_at is not None

    # the outbox retries: nothing changes
    again = await _patch(api, pair, plan, 1, status="eaten", event_id=eaten)
    assert again.status_code == 200
    assert again.json() == res.json()
    assert await _count(SlotEvent) == 1

    # a later change, then a stale replay of the first one: the later change stays
    res = await _patch(api, pair, plan, 1, status="skipped", event_id=skipped)
    assert res.json()["status"] == "skipped"
    res = await _patch(api, pair, plan, 1, status="eaten", event_id=eaten)
    assert res.status_code == 200 and res.json()["status"] == "skipped"
    assert await _count(SlotEvent) == 2

    # an event id reused for a different change is a client bug
    res = await _patch(api, pair, plan, 2, status="eaten", event_id=eaten)
    assert res.status_code == 409
    res = await _patch(api, pair, plan, 1, status="cooked", event_id=eaten)
    assert res.status_code == 409

    current = (await api.get("/v1/plans/current", headers=bearer(pair))).json()
    statuses = {s["position"]: s["status"] for d in current["plan_days"] for s in d["slots"]}
    assert statuses[1] == "skipped"
    assert statuses[2] == "planned"


EVENT = "6f1c2b9e-0d5a-4c3e-9a57-2f8e4b1d7c60"


@pytest.mark.parametrize(
    "body",
    [
        {"status": "planned", "event_id": EVENT},  # only cooked, eaten or skipped
        {"status": "eaten"},
        {"status": "eaten", "event_id": "not-a-uuid"},
        {"status": "eaten", "event_id": EVENT, "at": "2026-10-13T08:00:00Z"},
    ],
)
async def test_slot_status_body_is_checked(api: AsyncClient, apple: FakeApple, body: Json) -> None:
    pair = await login(api, apple)
    plan = await _create(api, pair)
    assert (await _patch(api, pair, plan, 0, **body)).status_code == 422


async def test_other_users_plan_is_not_found(api: AsyncClient, apple: FakeApple) -> None:
    owner = await login(api, apple, "apple-sub-owner")
    other = await login(api, apple, "apple-sub-other")
    plan = await _create(api, owner)

    assert (await api.get("/v1/plans/current", headers=bearer(other))).status_code == 404
    event = str(uuid.uuid4())
    res = await _patch(api, other, plan, 0, status="eaten", event_id=event)
    assert res.status_code == 404
    # a slot that doesn't exist looks the same
    res = await _patch(api, owner, plan, 99, status="eaten", event_id=event)
    assert res.status_code == 404
    res = await _patch(api, owner, {"id": str(uuid.uuid4())}, 0, status="eaten", event_id=event)
    assert res.status_code == 404
    assert await _count(SlotEvent) == 0

    # the owner can still use the same event id: nothing was recorded
    res = await _patch(api, owner, plan, 0, status="eaten", event_id=event)
    assert res.status_code == 200


async def test_account_deletion_removes_plans(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    plan = await _create(api, pair)
    res = await _patch(api, pair, plan, 0, status="cooked", event_id=str(uuid.uuid4()))
    assert res.status_code == 200
    assert (await api.delete("/v1/me", headers=bearer(pair))).status_code == 204
    assert await _count(MealPlan) == 0
    assert await _count(SlotEvent) == 0
