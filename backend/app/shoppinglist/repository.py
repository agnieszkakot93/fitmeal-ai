"""Building a plan's shopping list, keeping its checkmarks, and recording check events."""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from datetime import UTC, datetime

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.foods.models import FoodItem
from app.foods.vocab import CulinaryRole, FoodCategory
from app.nutrition.nutrients import Nutrients
from app.planner.result import DayPlan, Plan, PlannedMeal
from app.plans.models import MealPlan, PlanSlot
from app.recipes.models import Recipe, RecipeIngredient
from app.shopping.aggregate import (
    NOT_BOUGHT,
    FoodFacts,
    Lang,
    RecipeLine,
    ShoppingList,
    build_list,
    needs_from_plan,
)
from app.shoppinglist.models import ShoppingItemEvent, ShoppingListItem

_FOOD_DETAILS = (selectinload(FoodItem.portions), selectinload(FoodItem.packages))


def to_facts(food: FoodItem) -> FoodFacts:
    """The shopping list's view of a stored food; needs portions and packages loaded."""
    return FoodFacts(
        key=food.slug,
        name_en=food.name_en,
        name_pl=food.name_pl,
        category=FoodCategory(food.category),
        packages_g=tuple(p.size_g for p in food.packages),
        portions_g={p.unit: p.grams for p in food.portions},
        density_g_per_ml=food.density_g_per_ml,
        liquid=CulinaryRole.LIQUID in food.culinary_roles,
        bought=food.slug not in NOT_BOUGHT,
    )


def _lines(recipe: Recipe) -> list[RecipeLine]:
    return [
        RecipeLine(f"{i.position}:{i.food.slug}", i.food.slug, i.amount_g / recipe.servings)
        for i in recipe.ingredients
    ]


def _as_plan(slots: Sequence[PlanSlot]) -> Plan:
    """The planner's view of the stored slots, enough for ``needs_from_plan``."""
    by_day: dict[int, list[PlannedMeal]] = {}
    for s in slots:
        if s.recipe_id is None:  # the recipe was deleted since: nothing to buy for it
            continue
        meal = PlannedMeal(
            day=s.day,
            slot=s.slot,
            recipe_id=str(s.recipe_id),
            portion=s.portion,
            nutrition=Nutrients(s.kcal, s.protein_g, s.fat_g, s.carbs_g, s.fiber_g),
            cook_day=s.cook_day,
            eat_by_day=s.eat_by_day,
            from_batch=s.from_batch,
            leave_out=tuple(s.leave_out),
            labels=(),
        )
        by_day.setdefault(s.day, []).append(meal)
    return Plan(tuple(DayPlan(d, tuple(m)) for d, m in sorted(by_day.items())), notices=())


async def owned_plan(
    session: AsyncSession, user_id: uuid.UUID, plan_id: uuid.UUID
) -> MealPlan | None:
    """The plan with its recipes, ingredients and their foods, if the user owns it."""
    stmt = (
        select(MealPlan)
        .where(MealPlan.id == plan_id, MealPlan.user_id == user_id)
        .options(
            selectinload(MealPlan.slots)
            .selectinload(PlanSlot.recipe)
            .selectinload(Recipe.ingredients)
            .selectinload(RecipeIngredient.food)
            .options(*_FOOD_DETAILS)
        )
    )
    return (await session.scalars(stmt)).one_or_none()


async def sync(
    session: AsyncSession, plan: MealPlan, lang: Lang
) -> tuple[ShoppingList, dict[str, ShoppingListItem]]:
    """Rebuild the plan's list from its current slots and store it.

    Foods still on the list keep their row, so their id and checkmark; foods no
    longer needed are deleted, new ones start unchecked. Returns the list and
    the stored rows by food slug. Needs the plan loaded by :func:`owned_plan`.
    """
    recipes = {str(s.recipe.id): s.recipe for s in plan.slots if s.recipe is not None}
    foods = {i.food.slug: i.food for r in recipes.values() for i in r.ingredients}
    shopping = build_list(
        needs_from_plan(_as_plan(plan.slots), {k: _lines(r) for k, r in recipes.items()}),
        {slug: to_facts(f) for slug, f in foods.items()},
        lang,
    )
    grams = {foods[i.food].id: i.grams for i in shopping.items}
    await session.execute(
        delete(ShoppingListItem).where(
            ShoppingListItem.plan_id == plan.id, ShoppingListItem.food_id.not_in(grams)
        )
    )
    if grams:
        stmt = insert(ShoppingListItem).values(
            [{"plan_id": plan.id, "food_id": f, "grams": g} for f, g in grams.items()]
        )
        await session.execute(
            stmt.on_conflict_do_update(
                constraint="uq_shopping_items_plan_id_food_id",
                set_={"grams": stmt.excluded.grams},
            )
        )
    rows = await session.scalars(
        select(ShoppingListItem)
        .where(ShoppingListItem.plan_id == plan.id)
        .options(selectinload(ShoppingListItem.food))
        .execution_options(populate_existing=True)
    )
    return shopping, {r.food.slug: r for r in rows}


async def owned_item(
    session: AsyncSession, user_id: uuid.UUID, item_id: uuid.UUID
) -> ShoppingListItem | None:
    stmt = (
        select(ShoppingListItem)
        .join(MealPlan)
        .where(ShoppingListItem.id == item_id, MealPlan.user_id == user_id)
        .options(selectinload(ShoppingListItem.food).options(*_FOOD_DETAILS))
        .with_for_update(of=ShoppingListItem)
    )
    return (await session.scalars(stmt)).one_or_none()


class EventConflict(Exception):
    """The event id was already used for a different change."""


async def record_check(
    session: AsyncSession, item: ShoppingListItem, event_id: uuid.UUID, checked: bool
) -> None:
    """Apply a checkmark change once per event id; a replay of the same event changes nothing."""
    inserted = await session.scalar(
        insert(ShoppingItemEvent)
        .values(id=event_id, item_id=item.id, checked=checked)
        .on_conflict_do_nothing(index_elements=[ShoppingItemEvent.id])
        .returning(ShoppingItemEvent.id)
    )
    if inserted is None:
        seen = await session.get(ShoppingItemEvent, event_id)
        if seen is None or seen.item_id != item.id or seen.checked != checked:
            raise EventConflict
        return
    item.checked = checked
    item.checked_updated_at = datetime.now(UTC)
