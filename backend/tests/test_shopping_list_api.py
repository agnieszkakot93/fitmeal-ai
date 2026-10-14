"""Shopping list API against Postgres, on a plan from the real catalog and FDC snapshot."""

from __future__ import annotations

import math
import uuid
from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy import func, select, update
from sqlalchemy.orm import selectinload

from app.core.db import get_sessionmaker
from app.foods.models import FoodItem
from app.foods.vocab import FoodCategory
from app.plans.models import PlanSlot
from app.recipes.models import Recipe, RecipeIngredient
from app.shopping import display
from app.shopping.aggregate import NOT_BOUGHT
from app.shopping.display import Amount, DisplayUnit
from app.shoppinglist.models import ShoppingItemEvent, ShoppingListItem
from app.shoppinglist.router import pick_lang
from tests.test_auth import FakeApple, apple, apple_key, bearer, client, login
from tests.test_plans import _create, api, snapshot_catalog

__all__ = ["api", "apple", "apple_key", "client", "snapshot_catalog"]  # shared fixtures

Json = dict[str, Any]


async def _list(c: AsyncClient, pair: Json, plan_id: str, **params: str) -> Json:
    res = await c.get(f"/v1/plans/{plan_id}/shopping-list", params=params, headers=bearer(pair))
    assert res.status_code == 200, res.text
    body: Json = res.json()
    return body


async def _check(c: AsyncClient, pair: Json, item_id: str, checked: bool, event: str) -> Response:
    return await c.patch(
        f"/v1/shopping-items/{item_id}",
        json={"checked": checked, "event_id": event},
        headers=bearer(pair),
    )


def _items(shopping: Json) -> dict[str, Json]:
    return {i["food_slug"]: i for s in shopping["sections"] for i in s["items"]}


async def _expected_grams(plan_id: str) -> dict[str, float]:
    """Grams per food straight from the stored slots and recipes."""
    async with get_sessionmaker()() as session:
        slots = await session.scalars(
            select(PlanSlot)
            .where(PlanSlot.plan_id == uuid.UUID(plan_id))
            .options(
                selectinload(PlanSlot.recipe)
                .selectinload(Recipe.ingredients)
                .selectinload(RecipeIngredient.food)
            )
        )
        parts: dict[str, list[float]] = {}
        for slot in slots:
            assert slot.recipe is not None
            for i in slot.recipe.ingredients:
                if f"{i.position}:{i.food.slug}" not in slot.leave_out:
                    grams = i.amount_g / slot.recipe.servings * slot.portion
                    parts.setdefault(i.food.slug, []).append(grams)
    return {f: math.fsum(g) for f, g in parts.items() if f not in NOT_BOUGHT}


async def _count(model: type[ShoppingListItem] | type[ShoppingItemEvent]) -> int:
    async with get_sessionmaker()() as session:
        return int(await session.scalar(select(func.count()).select_from(model)) or 0)


async def test_auth_required(api: AsyncClient) -> None:
    assert (await api.get(f"/v1/plans/{uuid.uuid4()}/shopping-list")).status_code == 401
    res = await api.patch(
        f"/v1/shopping-items/{uuid.uuid4()}",
        json={"checked": True, "event_id": str(uuid.uuid4())},
    )
    assert res.status_code == 401


async def test_list_from_a_snapshot_catalog_plan(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    plan = await _create(api, pair)
    shopping = await _list(api, pair, plan["id"])

    assert shopping["plan_id"] == plan["id"] and shopping["lang"] == "en"
    sections = [s["category"] for s in shopping["sections"]]
    assert sections == [c.value for c in FoodCategory if c.value in sections]
    items = _items(shopping)
    expected = await _expected_grams(plan["id"])
    assert set(items) == set(expected)
    async with get_sessionmaker()() as session:
        foods = {
            f.slug: f
            for f in await session.scalars(
                select(FoodItem)
                .where(FoodItem.slug.in_(items))
                .options(selectinload(FoodItem.portions))
            )
        }
    for slug, item in items.items():
        food = foods[slug]
        assert item["grams"] == pytest.approx(expected[slug])
        assert item["name"] == food.name_en and item["category"] == food.category
        assert item["checked"] is False and item["checked_updated_at"] is None
        # rounded up: the list never under-buys
        amount = Amount(item["amount"]["value"], DisplayUnit(item["amount"]["unit"]))
        portions = {p.unit: p.grams for p in food.portions}
        each = portions.get("can") or portions.get("piece")
        bought = display.to_grams(amount, density_g_per_ml=food.density_g_per_ml, each_g=each)
        assert bought >= item["grams"] - 1e-6
        if item["packages"] is not None:
            assert item["packages"]["total_g"] >= item["grams"] - 1e-6
    # at least some foods come with package counts and counted units
    assert any(i["packages"] for i in items.values())
    assert any(i["amount"]["unit"] in ("piece", "can") for i in items.values())

    # reading again changes nothing: same ids, nothing duplicated
    again = await _list(api, pair, plan["id"])
    assert again == shopping
    assert await _count(ShoppingListItem) == len(items)


async def test_polish_names(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    plan = await _create(api, pair)
    en = _items(await _list(api, pair, plan["id"]))
    pl = await _list(api, pair, plan["id"], lang="pl")
    assert pl["lang"] == "pl"
    by_header = await api.get(
        f"/v1/plans/{plan['id']}/shopping-list",
        headers={**bearer(pair), "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8"},
    )
    assert by_header.json() == pl
    async with get_sessionmaker()() as session:
        names = dict((await session.execute(select(FoodItem.slug, FoodItem.name_pl))).all())
    for slug, item in _items(pl).items():
        assert item["name"] == names[slug]
        # the same stored rows in either language
        assert item["id"] == en[slug]["id"] and item["grams"] == en[slug]["grams"]


@pytest.mark.parametrize(
    ("lang", "header", "expected"),
    [
        (None, None, "en"),
        ("pl", "en", "pl"),
        (None, "pl", "pl"),
        (None, "PL-pl", "pl"),
        (None, "de-DE,de;q=0.9,pl;q=0.5,en;q=0.4", "pl"),
        (None, "en;q=0.5,pl;q=0.8", "pl"),
        (None, "pl;q=0,en;q=0.1", "en"),
        (None, "de, fr", "en"),
        (None, "pl;q=abc,en", "en"),
        (None, "*", "en"),
    ],
)
def test_pick_lang(lang: Any, header: str | None, expected: str) -> None:
    assert pick_lang(lang, header) == expected


async def test_unknown_lang_is_rejected(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    plan = await _create(api, pair)
    res = await api.get(
        f"/v1/plans/{plan['id']}/shopping-list", params={"lang": "de"}, headers=bearer(pair)
    )
    assert res.status_code == 422


async def test_check_replay_is_idempotent(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    plan = await _create(api, pair)
    first, second, *_ = _items(await _list(api, pair, plan["id"])).values()
    check, uncheck = str(uuid.uuid4()), str(uuid.uuid4())

    res = await _check(api, pair, first["id"], True, check)
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["checked"] is True and body["checked_updated_at"] is not None
    assert {k: v for k, v in body.items() if not k.startswith("checked")} == {
        k: v for k, v in first.items() if not k.startswith("checked")
    }

    # the outbox retries: nothing changes
    again = await _check(api, pair, first["id"], True, check)
    assert again.status_code == 200 and again.json() == body
    assert await _count(ShoppingItemEvent) == 1

    # a later change, then a stale replay of the first one: the later change stays
    res = await _check(api, pair, first["id"], False, uncheck)
    assert res.json()["checked"] is False
    res = await _check(api, pair, first["id"], True, check)
    assert res.status_code == 200 and res.json()["checked"] is False
    assert await _count(ShoppingItemEvent) == 2

    # an event id reused for a different change is a client bug
    assert (await _check(api, pair, second["id"], True, check)).status_code == 409
    assert (await _check(api, pair, first["id"], False, check)).status_code == 409

    # the names follow the requested language
    res = await api.patch(
        f"/v1/shopping-items/{second['id']}",
        params={"lang": "pl"},
        json={"checked": True, "event_id": str(uuid.uuid4())},
        headers=bearer(pair),
    )
    pl = _items(await _list(api, pair, plan["id"], lang="pl"))
    assert res.json() == pl[second["food_slug"]]
    assert pl[second["food_slug"]]["checked"] is True
    assert pl[first["food_slug"]]["checked"] is False


@pytest.mark.parametrize(
    "body",
    [
        {"checked": True},
        {"checked": "maybe", "event_id": str(uuid.UUID(int=1))},
        {"checked": True, "event_id": "not-a-uuid"},
        {"checked": True, "event_id": str(uuid.UUID(int=1)), "at": "2026-10-14T08:00:00Z"},
    ],
)
async def test_check_body_is_validated(api: AsyncClient, apple: FakeApple, body: Json) -> None:
    pair = await login(api, apple)
    plan = await _create(api, pair)
    item = next(iter(_items(await _list(api, pair, plan["id"])).values()))
    res = await api.patch(f"/v1/shopping-items/{item['id']}", json=body, headers=bearer(pair))
    assert res.status_code == 422
    assert all("input" not in error for error in res.json()["detail"])


async def test_other_users_list_is_not_found(api: AsyncClient, apple: FakeApple) -> None:
    owner = await login(api, apple, "apple-sub-owner")
    other = await login(api, apple, "apple-sub-other")
    plan = await _create(api, owner)
    item = next(iter(_items(await _list(api, owner, plan["id"])).values()))

    res = await api.get(f"/v1/plans/{plan['id']}/shopping-list", headers=bearer(other))
    assert res.status_code == 404
    res = await api.get(f"/v1/plans/{uuid.uuid4()}/shopping-list", headers=bearer(owner))
    assert res.status_code == 404
    event = str(uuid.uuid4())
    assert (await _check(api, other, item["id"], True, event)).status_code == 404
    # an item that doesn't exist looks the same
    assert (await _check(api, owner, str(uuid.uuid4()), True, event)).status_code == 404
    assert await _count(ShoppingItemEvent) == 0

    # the owner can still use the same event id: nothing was recorded
    assert (await _check(api, owner, item["id"], True, event)).status_code == 200


async def _set_slots(plan_id: str, **values: Any) -> dict[int, uuid.UUID | None]:
    """Change the stored plan, as a swap would; returns the old recipe per slot."""
    async with get_sessionmaker()() as session:
        rows = await session.execute(
            select(PlanSlot.id, PlanSlot.recipe_id).where(PlanSlot.plan_id == uuid.UUID(plan_id))
        )
        before = dict(rows.all())
        await session.execute(
            update(PlanSlot).where(PlanSlot.plan_id == uuid.UUID(plan_id)).values(**values)
        )
        await session.commit()
    return before


async def _restore(before: dict[int, uuid.UUID | None]) -> None:
    async with get_sessionmaker()() as session:
        for slot_id, recipe_id in before.items():
            await session.execute(
                update(PlanSlot).where(PlanSlot.id == slot_id).values(recipe_id=recipe_id)
            )
        await session.commit()


async def test_checkmarks_survive_regeneration(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    plan = await _create(api, pair)
    before = _items(await _list(api, pair, plan["id"]))
    first = plan["plan_days"][0]["slots"][0]
    async with get_sessionmaker()() as session:
        kept_foods = set(
            await session.scalars(
                select(FoodItem.slug)
                .join(RecipeIngredient)
                .where(RecipeIngredient.recipe_id == uuid.UUID(first["recipe_id"]))
            )
        )
    kept = next(i for slug, i in before.items() if slug in kept_foods)
    dropped = next(i for slug, i in before.items() if slug not in kept_foods)
    unchecked = next(i for slug, i in before.items() if slug in kept_foods and i != kept)
    for item in (kept, dropped):
        assert (await _check(api, pair, item["id"], True, str(uuid.uuid4()))).status_code == 200

    # every meal becomes the first recipe at one serving, nothing left out
    old = await _set_slots(
        plan["id"], recipe_id=uuid.UUID(first["recipe_id"]), portion=1.0, leave_out=[]
    )
    after = _items(await _list(api, pair, plan["id"]))
    assert set(after) <= kept_foods and dropped["food_slug"] not in after
    assert after[kept["food_slug"]]["id"] == kept["id"]
    assert after[kept["food_slug"]]["checked"] is True
    assert after[kept["food_slug"]]["grams"] == pytest.approx(
        (await _expected_grams(plan["id"]))[kept["food_slug"]]
    )
    assert after[unchecked["food_slug"]]["checked"] is False
    assert all(not i["checked"] for slug, i in after.items() if slug != kept["food_slug"])
    assert await _count(ShoppingListItem) == len(after)
    # the dropped item's events went with it, and its old id is gone
    assert await _count(ShoppingItemEvent) == 1
    res = await _check(api, pair, dropped["id"], False, str(uuid.uuid4()))
    assert res.status_code == 404

    # a food that comes back starts unchecked
    await _restore(old)
    back = _items(await _list(api, pair, plan["id"]))
    assert set(back) == set(before)
    assert back[dropped["food_slug"]]["checked"] is False
    assert back[kept["food_slug"]]["checked"] is True


async def test_deleted_recipe_drops_off(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    plan = await _create(api, pair)
    await _set_slots(plan["id"], recipe_id=None)
    assert (await _list(api, pair, plan["id"]))["sections"] == []
    assert await _count(ShoppingListItem) == 0


async def test_export_and_account_deletion(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    other = await login(api, apple, "apple-sub-other")
    plan = await _create(api, pair)
    theirs = await _create(api, other)
    items = _items(await _list(api, pair, plan["id"]))
    await _list(api, other, theirs["id"])
    item = next(iter(items.values()))
    event = str(uuid.uuid4())
    assert (await _check(api, pair, item["id"], True, event)).status_code == 200

    res = await api.get("/v1/me/export", headers=bearer(pair))
    assert res.status_code == 200
    [exported] = res.json()["plans"]
    stored = {i["food_slug"]: i for i in exported["shopping_items"]}
    assert set(stored) == set(items)
    assert stored[item["food_slug"]]["id"] == item["id"]
    assert stored[item["food_slug"]]["checked"] is True
    assert [e["id"] for e in stored[item["food_slug"]]["events"]] == [event]
    assert all(i["plan_id"] == plan["id"] for i in exported["shopping_items"])

    their_count = len(_items(await _list(api, other, theirs["id"])))
    assert (await api.delete("/v1/me", headers=bearer(pair))).status_code == 204
    assert await _count(ShoppingListItem) == their_count
    assert await _count(ShoppingItemEvent) == 0
