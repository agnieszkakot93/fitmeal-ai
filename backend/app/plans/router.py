"""Plans: generate, read the current one, and mark meals cooked, eaten or skipped.

Sign-in is required throughout; there is no anonymous plan endpoint (D12).
``POST /v1/plans`` uses the stored health profile when there is one and the
health-data consent is active (D13); otherwise the request's profile snapshot,
used in memory only (D8 fallback).
"""

from __future__ import annotations

import asyncio
import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import CurrentUser
from app.auth.routing import HideInputRoute
from app.core.db import get_session
from app.nutrition.nutrients import Nutrients
from app.planner.plan import plan as build_plan
from app.planner.result import Infeasible, Plan
from app.plans import repository
from app.plans.models import MealPlan, PlanSlot, SlotStatus
from app.plans.schemas import (
    BlockerOut,
    DayOut,
    InfeasibleOut,
    InvalidBodyOut,
    PlanIn,
    PlanOut,
    SlotOut,
    SlotStatusIn,
    SuggestionOut,
    TargetsOut,
)
from app.profile import service as profile_service
from app.recipes.schemas import nutrients_out
from app.variants import slots as slot_swaps
from app.variants.schemas import (
    RebalanceApplyIn,
    SwapIn,
    SwapOptionsIn,
    SwapOptionsOut,
    SwapOut,
)

router = APIRouter(prefix="/v1/plans", tags=["plans"], route_class=HideInputRoute)

Session = Annotated[AsyncSession, Depends(get_session)]

_PLAN_NOT_FOUND = "plan not found"
# the shape of a validation error, as the 422 response documents
_NO_PROFILE = [
    {
        "type": "missing",
        "loc": ["body", "profile"],
        "msg": "no stored profile with health-data consent: send a profile snapshot",
    }
]
_INFEASIBLE: dict[int | str, dict[str, Any]] = {
    status.HTTP_422_UNPROCESSABLE_CONTENT: {
        "model": InfeasibleOut | InvalidBodyOut,
        "description": "No plan fits the profile's hard constraints, or the body is invalid",
    }
}


def _nutrients(slot: PlanSlot) -> Nutrients:
    return Nutrients(
        kcal=slot.kcal,
        protein_g=slot.protein_g,
        fat_g=slot.fat_g,
        carbs_g=slot.carbs_g,
        fiber_g=slot.fiber_g,
    )


def _slot_out(slot: PlanSlot, labels: dict[tuple[int, str], tuple[str, ...]]) -> SlotOut:
    recipe = slot.recipe
    return SlotOut(
        position=slot.position,
        day=slot.day,
        slot=slot.slot,
        meal_type=slot.meal_type,
        recipe_id=slot.recipe_id,
        recipe_slug=recipe.slug if recipe else None,
        title_en=recipe.title_en if recipe else None,
        title_pl=recipe.title_pl if recipe else None,
        portion=slot.portion,
        nutrition=nutrients_out(_nutrients(slot)),
        cook_day=slot.cook_day,
        eat_by_day=slot.eat_by_day,
        from_batch=slot.from_batch,
        leave_out=slot.leave_out,
        labels=list(labels.get((slot.day, slot.slot), ())),
        status=slot.status,
        status_updated_at=slot.status_updated_at,
    )


def _plan_out(
    plan: MealPlan, labels: dict[tuple[int, str], tuple[str, ...]] | None = None
) -> PlanOut:
    by_day: dict[int, list[PlanSlot]] = {}
    for slot in plan.slots:
        by_day.setdefault(slot.day, []).append(slot)
    return PlanOut(
        id=plan.id,
        created_at=plan.created_at,
        days=plan.days,
        prep_days=plan.prep_days,
        targets=TargetsOut(daily_kcal=plan.daily_kcal, protein_min_g=plan.protein_min_g),
        notices=plan.notices,
        relaxed=plan.relaxed,
        plan_days=[
            DayOut(
                day=day,
                totals=nutrients_out(Nutrients.total([_nutrients(s) for s in slots])),
                slots=[_slot_out(s, labels or {}) for s in slots],
            )
            for day, slots in sorted(by_day.items())
        ],
    )


def _infeasible_out(report: Infeasible) -> InfeasibleOut:
    return InfeasibleOut(
        status=report.status,
        message=report.message,
        blockers=[BlockerOut(kind=b.kind, message=b.message, meal=b.meal) for b in report.blockers],
        suggestions=[
            SuggestionOut(action=s.action, message=s.message, value=s.value)
            for s in report.suggestions
        ],
    )


@router.post("", response_model=PlanOut, status_code=status.HTTP_201_CREATED, responses=_INFEASIBLE)
async def create_plan(body: PlanIn, user: CurrentUser, session: Session) -> PlanOut | JSONResponse:
    """Generate a plan, save it as the current plan and return it.

    Built from the stored profile when there is one and health-data consent is
    active, else from the request's profile snapshot.
    """
    user_id = user.id  # the rollback below expires every loaded row
    source = await profile_service.for_planning(session, user_id) or body.profile
    if source is None:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, _NO_PROFILE)
    profile = body.to_profile(source)
    recipes = await repository.candidates(session, user_id)
    candidates = [repository.to_candidate(r) for r in recipes.values()]
    recipe_ids = {key: r.id for key, r in recipes.items()}
    # don't hold a connection while solving
    await session.rollback()
    # CP-SAT is CPU-bound for up to its time limit: keep the event loop free
    result = await asyncio.to_thread(build_plan, candidates, profile)
    if isinstance(result, Infeasible):
        return JSONResponse(
            _infeasible_out(result).model_dump(mode="json"),
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )
    saved = repository.save(session, user_id, profile, result, recipe_ids)
    await session.commit()
    return _plan_out(await repository.get(session, saved.id), _labels(result))


def _labels(result: Plan) -> dict[tuple[int, str], tuple[str, ...]]:
    return {(m.day, m.slot): m.labels for m in result.meals}


@router.get("/current", response_model=PlanOut)
async def current_plan(user: CurrentUser, session: Session) -> PlanOut:
    """The user's latest plan."""
    plan = await repository.current(session, user.id)
    if plan is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, _PLAN_NOT_FOUND)
    return _plan_out(plan)


@router.patch("/{plan_id}/slots/{slot}", response_model=SlotOut)
async def set_slot_status(
    plan_id: uuid.UUID, slot: int, body: SlotStatusIn, user: CurrentUser, session: Session
) -> SlotOut:
    """Mark a meal cooked, eaten or skipped.

    Idempotent per ``event_id``: replaying an event (an offline outbox retrying)
    returns the slot unchanged. Reusing an event id for a different change is a 409.
    """
    found = await repository.owned_slot(session, user.id, plan_id, slot)
    if found is None:
        # another user's plan looks the same as a missing one
        raise HTTPException(status.HTTP_404_NOT_FOUND, "slot not found")
    try:
        await repository.record_status(session, found, body.event_id, SlotStatus(body.status))
    except repository.EventConflict:
        await session.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, "event id already used for a different change"
        ) from None
    await session.commit()
    await session.refresh(found, ["recipe"])
    return _slot_out(found, {})


_SLOT_ERRORS: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {"description": "No such plan or slot for this user"},
    status.HTTP_409_CONFLICT: {"description": "The meal is already eaten or skipped"},
}


@router.post(
    "/{plan_id}/slots/{slot}/swap-options", response_model=SwapOptionsOut, responses=_SLOT_ERRORS
)
async def swap_options(
    plan_id: uuid.UUID, slot: int, body: SwapOptionsIn, user: CurrentUser, session: Session
) -> SwapOptionsOut:
    """Recipes that could replace the meal, best fit first, sized like it (PRD §8.6).

    Only recipes that pass the profile's hard constraints are offered. The
    profile is the stored one with health-data consent, else the body's snapshot.
    """
    found, options = await slot_swaps.options(session, user.id, plan_id, slot, body)
    out = SwapOptionsOut(slot=_slot_out(found, {}), options=options)
    await session.rollback()  # nothing changed; release the plan lock
    return out


@router.post("/{plan_id}/slots/{slot}/swap", response_model=SwapOut, responses=_SLOT_ERRORS)
async def swap_slot(
    plan_id: uuid.UUID, slot: int, body: SwapIn, user: CurrentUser, session: Session
) -> SwapOut:
    """Put another recipe in the meal and propose a rebalance of the day's other meals.

    The swap is saved; the rebalance is only a proposal, applied through
    `POST /v1/plans/{id}/rebalance/apply` (PRD §8.6).
    """
    _, found, proposal = await slot_swaps.swap(session, user.id, plan_id, slot, body)
    out = SwapOut(slot=_slot_out(found, {}), rebalance=proposal)
    await session.commit()
    return out


@router.post("/{plan_id}/rebalance/apply", response_model=PlanOut, responses=_SLOT_ERRORS)
async def apply_rebalance(
    plan_id: uuid.UUID, body: RebalanceApplyIn, user: CurrentUser, session: Session
) -> PlanOut:
    """Apply the portion adjustments the user accepted from a rebalance proposal.

    Each may move a meal's portion by at most 20%, never on an eaten or skipped
    meal, and never take the day below 1200 kcal.
    """
    plan = await slot_swaps.apply_rebalance(session, user.id, plan_id, body)
    await session.commit()
    return _plan_out(await repository.get(session, plan.id))
