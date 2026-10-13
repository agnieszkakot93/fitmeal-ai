"""Loading candidates, saving plans and recording meal status."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.foods.models import FoodItem
from app.foods.repository import to_allergens
from app.planner.inputs import Candidate, Profile
from app.planner.result import Plan
from app.plans.models import MealPlan, PlanSlot, SlotEvent, SlotStatus
from app.recipes import repository as recipes_repo
from app.recipes.models import Recipe, RecipeIngredient
from app.recipes.safety import CheckLine


def to_candidate(recipe: Recipe) -> Candidate:
    """The planner's view of a stored recipe; needs ingredients and foods loaded."""
    return Candidate(
        id=recipe.slug or str(recipe.id),
        tags=frozenset(recipe.tags),
        per_serving=recipes_repo.compute_nutrition(recipe).per_serving,
        servings=recipe.servings,
        fridge_days=recipe.fridge_days or 0,
        freezer_friendly=recipe.freezer_friendly,
        meal_prep_score=recipe.meal_prep_score or 0,
        total_minutes=(recipe.prep_minutes or 0) + (recipe.cook_minutes or 0),
        equipment=frozenset(recipe.equipment),
        allergen_lines=tuple(
            CheckLine(f"{i.position}:{i.food.slug}", to_allergens(i.food), i.optional)
            for i in recipe.ingredients
        ),
        ingredient_ids=frozenset(i.food.slug for i in recipe.ingredients),
    )


async def candidates(session: AsyncSession, user_id: uuid.UUID) -> dict[str, Recipe]:
    """Catalog recipes and the user's own, by candidate id. Only those with nutrition."""
    stmt = (
        select(Recipe)
        .where(
            or_(Recipe.owner_user_id.is_(None), Recipe.owner_user_id == user_id),
            Recipe.kcal.is_not(None),
        )
        .options(
            selectinload(Recipe.ingredients)
            .selectinload(RecipeIngredient.food)
            .options(selectinload(FoodItem.portions), selectinload(FoodItem.aliases))
        )
    )
    recipes = await session.scalars(stmt)
    return {r.slug or str(r.id): r for r in recipes}


def save(
    session: AsyncSession,
    user_id: uuid.UUID,
    profile: Profile,
    result: Plan,
    recipe_ids: dict[str, uuid.UUID],
) -> MealPlan:
    meal_types = {m.name: m.meal_type for m in profile.meals}
    order = {m.name: i for i, m in enumerate(profile.meals)}
    plan = MealPlan(
        user_id=user_id,
        days=profile.days,
        prep_days=profile.prep_days,
        daily_kcal=profile.daily_kcal,
        protein_min_g=profile.protein_min_g,
        notices=list(result.notices),
        relaxed=sorted(r.value for r in result.relaxed),
    )
    for meal in result.meals:
        n = meal.nutrition
        plan.slots.append(
            PlanSlot(
                position=meal.day * len(profile.meals) + order[meal.slot],
                day=meal.day,
                slot=meal.slot,
                meal_type=meal_types[meal.slot].value,
                recipe_id=recipe_ids[meal.recipe_id],
                portion=meal.portion,
                kcal=n.kcal,
                protein_g=n.protein_g,
                fat_g=n.fat_g,
                carbs_g=n.carbs_g,
                fiber_g=n.fiber_g,
                cook_day=meal.cook_day,
                eat_by_day=meal.eat_by_day,
                from_batch=meal.from_batch,
                leave_out=list(meal.leave_out),
            )
        )
    plan.slots.sort(key=lambda s: s.position)
    session.add(plan)
    return plan


_WITH_SLOTS = selectinload(MealPlan.slots).selectinload(PlanSlot.recipe)


async def get(session: AsyncSession, plan_id: uuid.UUID) -> MealPlan:
    stmt = (
        select(MealPlan)
        .where(MealPlan.id == plan_id)
        .options(_WITH_SLOTS)
        .execution_options(populate_existing=True)
    )
    return (await session.scalars(stmt)).one()


async def current(session: AsyncSession, user_id: uuid.UUID) -> MealPlan | None:
    """The user's latest plan."""
    stmt = (
        select(MealPlan)
        .where(MealPlan.user_id == user_id)
        .order_by(MealPlan.created_at.desc(), MealPlan.id)
        .limit(1)
        .options(_WITH_SLOTS)
    )
    return (await session.scalars(stmt)).one_or_none()


async def owned_slot(
    session: AsyncSession, user_id: uuid.UUID, plan_id: uuid.UUID, position: int
) -> PlanSlot | None:
    stmt = (
        select(PlanSlot)
        .join(MealPlan)
        .where(MealPlan.user_id == user_id, PlanSlot.plan_id == plan_id)
        .where(PlanSlot.position == position)
        .with_for_update(of=PlanSlot)
    )
    return (await session.scalars(stmt)).one_or_none()


class EventConflict(Exception):
    """The event id was already used for a different change."""


async def record_status(
    session: AsyncSession, slot: PlanSlot, event_id: uuid.UUID, status: SlotStatus
) -> None:
    """Apply a status change once per event id; a replay of the same event changes nothing."""
    inserted = await session.scalar(
        insert(SlotEvent)
        .values(id=event_id, slot_id=slot.id, status=status.value)
        .on_conflict_do_nothing(index_elements=[SlotEvent.id])
        .returning(SlotEvent.id)
    )
    if inserted is None:
        seen = await session.get(SlotEvent, event_id)
        if seen is None or seen.slot_id != slot.id or seen.status != status.value:
            raise EventConflict
        return
    slot.status = status.value
    slot.status_updated_at = datetime.now(UTC)
