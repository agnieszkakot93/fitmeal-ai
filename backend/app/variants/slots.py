"""Meal swaps in a plan slot and the rebalance of its day (PRD §8.6).

Swap options are the planner's own candidates: the hard filter
(:func:`app.planner.filter.screen`, double-checked with
:func:`app.recipes.safety.check`) and the slot score
(:func:`app.planner.score.score`), sized like the meal they replace. A swap is
applied when the user confirms it; the rebalance that follows is only a
proposal until ``rebalance/apply``. Meals marked eaten or skipped never change.
"""

from __future__ import annotations

import uuid
from collections.abc import Collection, Sequence
from dataclasses import dataclass

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.nutrition.nutrients import Nutrients
from app.planner.filter import Screened, screen
from app.planner.inputs import KCAL_FLOOR, Candidate, MealSlot, MealType, Profile
from app.planner.plan import _label as label
from app.planner.score import score
from app.plans import repository as plans_repo
from app.plans.models import MealPlan, PlanSlot, SlotStatus
from app.plans.schemas import ProfileIn, to_profile
from app.profile import service as profile_service
from app.recipes.models import Recipe
from app.recipes.safety import check
from app.recipes.schemas import nutrients_out
from app.variants import rebalance
from app.variants.models import PlanSlotVariant
from app.variants.schemas import (
    AdjustmentOut,
    RebalanceApplyIn,
    RebalanceOut,
    SwapIn,
    SwapOptionOut,
    SwapOptionsIn,
)

LOCKED = frozenset({SlotStatus.EATEN.value, SlotStatus.SKIPPED.value})
# plan portions are quarters of a serving, 0.5x to 2x (app.planner.solve.PORTIONS)
MIN_QUARTERS, MAX_QUARTERS = 2, 8

# the shape of a validation error, as the 422 response documents
NO_PROFILE = [
    {
        "type": "missing",
        "loc": ["body", "profile"],
        "msg": "no stored profile with health-data consent: send a profile snapshot",
    }
]


# ── pure ────────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Choice:
    screened: Screened
    portion: float
    nutrition: Nutrients
    score: int


def portion_for(kcal: float, per_serving_kcal: float) -> float:
    """The quarter-serving portion closest to ``kcal``, 0.5x to 2x."""
    if per_serving_kcal <= 0:
        return 1.0
    quarters = round(4 * kcal / per_serving_kcal)
    return min(max(quarters, MIN_QUARTERS), MAX_QUARTERS) / 4


def meal_slot(profile: Profile, slot: PlanSlot, daily_kcal: float) -> MealSlot:
    """The profile's meal for the slot; a slot the profile no longer has keeps its size."""
    found = next((m for m in profile.meals if m.name == slot.slot), None)
    if found is not None:
        return found
    share = min(1.0, max(0.01, slot.kcal / daily_kcal))
    return MealSlot(slot.slot, MealType(slot.meal_type), share)


def safe(screened: Screened, profile: Profile) -> bool:
    """Passes the planner's hard filter, and the recipe exclusion check agrees."""
    lines = screened.candidate.allergen_lines
    hard = profile.hard_exclusions
    if not screened.allowed or (hard and not lines):
        return False
    return not check(lines, hard).blocked


def rank(
    candidates: Sequence[Candidate],
    profile: Profile,
    meal: MealSlot,
    size_kcal: float,
    exclude: Collection[str] = (),
    limit: int | None = None,
) -> list[Choice]:
    """Safe candidates for the meal, best fit first, each sized to ``size_kcal``."""
    choices = []
    for candidate in candidates:
        if candidate.id in exclude or not candidate.fits(meal.meal_type):
            continue
        screened = screen(candidate, profile)
        if not safe(screened, profile):
            continue
        portion = portion_for(size_kcal, candidate.per_serving.kcal)
        choices.append(
            Choice(
                screened,
                portion,
                candidate.per_serving.scale(portion),
                score(screened, meal, profile).total,
            )
        )
    choices.sort(
        key=lambda c: (-c.score, abs(c.nutrition.kcal - size_kcal), c.screened.candidate.id)
    )
    return choices[:limit]


def nutrients(slot: PlanSlot) -> Nutrients:
    return Nutrients(slot.kcal, slot.protein_g, slot.fat_g, slot.carbs_g, slot.fiber_g)


def set_nutrition(slot: PlanSlot, n: Nutrients) -> None:
    slot.kcal, slot.protein_g, slot.fat_g = n.kcal, n.protein_g, n.fat_g
    slot.carbs_g, slot.fiber_g = n.carbs_g, n.fiber_g


def _message(p: rebalance.Proposal) -> str:
    if p.within_tolerance and not p.needed:
        return "The day is within its targets."
    if p.within_tolerance:
        return "Adjusting the other meals' portions brings the day back within its targets."
    parts = []
    if p.kcal_off > 0:
        parts.append(f"about {round(p.kcal_off)} kcal over your target")
    elif p.kcal_off < 0:
        parts.append(f"about {round(-p.kcal_off)} kcal under your target")
    if p.protein_short_g > 0:
        parts.append(f"{round(p.protein_short_g)} g short of your protein minimum")
    day = "The day" if not p.needed else "Even with these changes, the day"
    return f"{day} will be {' and '.join(parts)}."


def proposal(plan: MealPlan, day: int, fixed: Collection[int] = ()) -> RebalanceOut:
    """The day's rebalance proposal; locked and ``fixed`` meals stay as they are."""
    slots = [s for s in plan.slots if s.day == day]
    meals = [
        rebalance.Meal(
            s.position,
            s.portion,
            nutrients(s),
            adjustable=s.status not in LOCKED and s.position not in fixed,
        )
        for s in slots
    ]
    p = rebalance.propose(meals, plan.daily_kcal, plan.protein_min_g)
    names = {s.position: s.slot for s in slots}
    return RebalanceOut(
        plan_id=plan.id,
        day=day,
        needed=p.needed,
        within_tolerance=p.within_tolerance,
        totals_before=nutrients_out(p.before),
        totals_after=nutrients_out(p.after),
        kcal_off=round(p.kcal_off, 1),
        protein_short_g=round(p.protein_short_g, 1),
        adjustments=[
            AdjustmentOut(
                slot=a.position,
                slot_name=names[a.position],
                portion_from=a.portion_from,
                portion_to=a.portion_to,
                delta=nutrients_out(a.delta),
            )
            for a in p.adjustments
        ],
        message=_message(p),
    )


# ── database ────────────────────────────────────────────────────────────────


def _not_found(what: str) -> HTTPException:
    # another user's plan looks the same as a missing one
    return HTTPException(status.HTTP_404_NOT_FOUND, f"{what} not found")


async def owned_plan(session: AsyncSession, user_id: uuid.UUID, plan_id: uuid.UUID) -> MealPlan:
    """The user's plan with its slots, locked for the change; 404 for anyone else's."""
    plan = (
        await session.scalars(
            select(MealPlan)
            .where(MealPlan.id == plan_id, MealPlan.user_id == user_id)
            .options(selectinload(MealPlan.slots).selectinload(PlanSlot.recipe))
            .with_for_update(of=MealPlan)
            .execution_options(populate_existing=True)
        )
    ).one_or_none()
    if plan is None:
        raise _not_found("plan")
    return plan


def find_slot(plan: MealPlan, position: int) -> PlanSlot:
    found = next((s for s in plan.slots if s.position == position), None)
    if found is None:
        raise _not_found("slot")
    return found


async def _profile(
    session: AsyncSession, user_id: uuid.UUID, plan: MealPlan, snapshot: ProfileIn | None
) -> Profile:
    source = await profile_service.for_planning(session, user_id) or snapshot
    if source is None:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, NO_PROFILE)
    return to_profile(source, plan.days, plan.prep_days)


async def _candidates(
    session: AsyncSession, user_id: uuid.UUID
) -> tuple[list[Candidate], dict[str, Recipe]]:
    recipes = await plans_repo.candidates(session, user_id)
    return [plans_repo.to_candidate(r) for r in recipes.values()], recipes


def _day_ids(plan: MealPlan, slot: PlanSlot, with_slot: bool) -> set[str]:
    """Candidate ids of the day's recipes: a recipe at most once a day."""
    return {
        s.recipe.slug or str(s.recipe.id)
        for s in plan.slots
        if s.day == slot.day and s.recipe is not None and (with_slot or s is not slot)
    }


async def options(
    session: AsyncSession,
    user_id: uuid.UUID,
    plan_id: uuid.UUID,
    position: int,
    body: SwapOptionsIn,
) -> tuple[PlanSlot, list[SwapOptionOut]]:
    plan = await owned_plan(session, user_id, plan_id)
    slot = find_slot(plan, position)
    profile = await _profile(session, user_id, plan, body.profile)
    candidates, recipes = await _candidates(session, user_id)
    current = nutrients(slot)
    day = Nutrients.total([nutrients(s) for s in plan.slots if s.day == slot.day])
    ranked = rank(
        candidates,
        profile,
        meal_slot(profile, slot, plan.daily_kcal),
        slot.kcal,
        exclude=_day_ids(plan, slot, with_slot=True),
        limit=body.limit,
    )
    out = []
    for choice in ranked:
        c = choice.screened.candidate
        recipe = recipes[c.id]
        delta = choice.nutrition + current.scale(-1)
        out.append(
            SwapOptionOut(
                recipe_id=recipe.id,
                recipe_slug=recipe.slug,
                title_en=recipe.title_en,
                title_pl=recipe.title_pl,
                portion=choice.portion,
                nutrition=nutrients_out(choice.nutrition),
                delta=nutrients_out(delta),
                day_totals=nutrients_out(day + delta),
                total_minutes=c.total_minutes,
                leave_out=list(choice.screened.leave_out),
                labels=[label(p) for p in choice.screened.penalties],
                score=choice.score,
            )
        )
    return slot, out


async def swap(
    session: AsyncSession, user_id: uuid.UUID, plan_id: uuid.UUID, position: int, body: SwapIn
) -> tuple[MealPlan, PlanSlot, RebalanceOut]:
    """Put another recipe in the slot; returns the day's rebalance proposal (not applied)."""
    plan = await owned_plan(session, user_id, plan_id)
    slot = find_slot(plan, position)
    if slot.status in LOCKED:
        raise HTTPException(status.HTTP_409_CONFLICT, f"the meal is already {slot.status}")
    profile = await _profile(session, user_id, plan, body.profile)
    candidates, recipes = await _candidates(session, user_id)
    by_id = {r.id: c for c, r in zip(candidates, recipes.values(), strict=True)}
    candidate = by_id.get(body.recipe_id)
    if candidate is None:
        raise _not_found("recipe")
    ranked = rank(
        [candidate],
        profile,
        meal_slot(profile, slot, plan.daily_kcal),
        slot.kcal,
        exclude=_day_ids(plan, slot, with_slot=False),
    )
    if not ranked:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "the recipe doesn't fit this meal: wrong meal type, already on this day, or "
            "blocked by the profile's hard constraints",
        )
    choice = ranked[0]
    portion = body.portion if body.portion is not None else choice.portion
    slot.recipe_id = body.recipe_id
    slot.recipe = recipes[candidate.id]
    slot.portion = portion
    set_nutrition(slot, candidate.per_serving.scale(portion))
    slot.leave_out = list(choice.screened.leave_out)
    # cooked fresh for this day, out of any batch; a cooked mark was for the old recipe
    slot.cook_day = slot.eat_by_day = slot.day
    slot.from_batch = False
    slot.status = SlotStatus.PLANNED.value
    slot.status_updated_at = None
    await session.execute(delete(PlanSlotVariant).where(PlanSlotVariant.slot_id == slot.id))
    return plan, slot, proposal(plan, slot.day, {*body.fixed, slot.position})


async def apply_rebalance(
    session: AsyncSession, user_id: uuid.UUID, plan_id: uuid.UUID, body: RebalanceApplyIn
) -> MealPlan:
    """Apply the adjustments the user accepted, each within ±20% of the meal's portion."""
    plan = await owned_plan(session, user_id, plan_id)
    changes = []
    for adjustment in body.adjustments:
        slot = find_slot(plan, adjustment.slot)
        if slot.day != body.day:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "slot is on another day")
        if slot.status in LOCKED:
            raise HTTPException(status.HTTP_409_CONFLICT, f"the meal is already {slot.status}")
        factor = adjustment.portion / slot.portion
        if abs(factor - 1) > rebalance.MAX_CHANGE + 1e-6:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT, "a portion may change by at most 20%"
            )
        changes.append((slot, adjustment.portion, nutrients(slot).scale(factor)))
    before = sum(s.kcal for s in plan.slots if s.day == body.day)
    after = before + sum(n.kcal - s.kcal for s, _, n in changes)
    if after < KCAL_FLOOR and after < before:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT, "a rebalance never brings a day below 1200 kcal"
        )
    for slot, portion, n in changes:
        slot.portion = portion
        set_nutrition(slot, n)
    return plan
