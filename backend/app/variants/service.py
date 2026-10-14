"""Saving personalized recipes as variants and applying ingredient swaps to them.

The profile comes from the account when health-data consent is active (D13),
else from the request's snapshot, used in memory only (D8 fallback). A variant
stores the meal target it was computed for, never the exclusions; a left-out
ingredient's explanation doesn't say why for the same reason.
"""

from __future__ import annotations

import uuid
from collections.abc import Mapping, Sequence
from dataclasses import asdict
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.foods import repository as foods_repo
from app.foods.models import FoodItem
from app.foods.repository import to_allergens, to_facts, to_substitution_food
from app.nutrition.allergens import Exclusion
from app.nutrition.nutrients import Nutrients, for_grams
from app.optimizer.substitute import options
from app.optimizer.transform import KCAL_TOLERANCE_ROUNDED, Reason, Target, misses
from app.plans.models import MealPlan, PlanSlot
from app.profile import service as profile_service
from app.recipes import repository as recipes_repo
from app.recipes.models import Recipe, RecipeVariant
from app.recipes.schemas import (
    ChangeReason,
    Exclusions,
    ExplanationOut,
    FoodRef,
    MealTarget,
    MissOut,
    PersonalizeOut,
    SaveIn,
    nutrients_out,
    to_exclusions,
)
from app.variants import explain, slots
from app.variants import lines as vlines
from app.variants.explain import Explanation
from app.variants.lines import VariantLine
from app.variants.models import PlanSlotVariant
from app.variants.schemas import (
    SlotRefOut,
    SubstituteIn,
    SubstituteOut,
    VariantLineOut,
    VariantOut,
)

# how many ranked substitutes a named pick is looked up in
MAX_OPTIONS = 50


async def exclusions(
    session: AsyncSession, user_id: uuid.UUID | None, snapshot: Exclusions
) -> list[Exclusion]:
    """The stored profile's exclusions with consent, else the request's snapshot."""
    stored = await profile_service.for_planning(session, user_id) if user_id else None
    return to_exclusions(stored.exclusions if stored is not None else snapshot)


# ── explanations ────────────────────────────────────────────────────────────


def explanation_out(e: Explanation) -> ExplanationOut:
    return ExplanationOut(
        key=e.key,
        kind=e.kind,
        message=e.message,
        delta=nutrients_out(e.delta),
        reason=ChangeReason(e.reason.value) if e.reason else None,
    )


def _explanation_json(e: Explanation) -> dict[str, Any]:
    return explanation_out(e).model_dump(mode="json")


def _per_100g(food: FoodItem) -> Nutrients:
    return to_facts(food).per_100g


def _diff(old: FoodItem, old_g: float, new: FoodItem, new_g: float) -> Nutrients:
    return for_grams(_per_100g(new), new_g) + for_grams(_per_100g(old), old_g).scale(-1)


def explain_personalized(
    recipe: Recipe, out: PersonalizeOut, foods: Mapping[str, FoodItem]
) -> list[Explanation]:
    """One explanation per changed ingredient of a personalize proposal."""
    changes = {c.key: c for c in out.changes}
    engine = {line.key: line for line in recipes_repo.transform_lines(recipe)}
    result = []
    for p in out.ingredients:
        old = foods[p.original_food]
        name = old.name_en
        if p.removed or p.grams == 0:
            delta = for_grams(_per_100g(old), p.original_g).scale(-1)
            result.append(explain.left_out(p.key, name, p.original_g, delta))
        elif p.swapped:
            new = foods[p.food.slug]
            role = engine[p.key].role
            result.append(
                explain.swap(
                    p.key,
                    name,
                    p.original_g,
                    new.name_en,
                    p.grams,
                    role,
                    _diff(old, p.original_g, new, p.grams),
                )
            )
        elif (change := changes.get(p.key)) is not None and change.grams != change.original_g:
            reason = Reason(change.reason.value)
            delta = _diff(old, change.original_g, old, change.grams)
            result.append(
                explain.amount(p.key, name, change.original_g, change.grams, delta, reason)
            )
    return result


# ── variants ────────────────────────────────────────────────────────────────


def _lines(recipe: Recipe, out: PersonalizeOut) -> list[VariantLine]:
    engine = {line.key: line for line in recipes_repo.transform_lines(recipe)}
    return [
        VariantLine(
            key=p.key,
            position=p.position,
            food=p.food.slug,
            original_food=p.original_food,
            original_g=p.original_g,
            grams=p.grams,
            role=engine[p.key].role,
            optional=engine[p.key].optional,
            removed=p.removed or p.grams == 0,
            swapped=p.swapped,
        )
        for p in out.ingredients
    ]


def _target(t: MealTarget) -> Target:
    return Target(kcal=t.kcal, protein_min_g=t.protein_min_g, fat_g=t.fat_g, carbs_g=t.carbs_g)


def _nutrition_json(
    per_serving: Nutrients, original: Nutrients, target: MealTarget
) -> dict[str, Any]:
    missed = misses(_target(target), per_serving, KCAL_TOLERANCE_ROUNDED)
    return {
        "per_serving": asdict(per_serving),
        "original": asdict(original),
        "on_target": not missed,
        "misses": [
            MissOut(
                metric=m.metric, target=round(m.target, 1), actual=round(m.actual, 1)
            ).model_dump(mode="json")
            for m in missed
        ],
    }


async def save_personalized(
    session: AsyncSession,
    user_id: uuid.UUID,
    recipe: Recipe,
    target: MealTarget,
    out: PersonalizeOut,
    save: SaveIn,
    explanations: Sequence[Explanation],
    foods: Mapping[str, FoodItem],
) -> RecipeVariant:
    """Store the proposal as the user's variant and, if asked, cook it in a plan slot."""
    lines = _lines(recipe, out)
    per_serving = vlines.nutrition(lines, {s: _per_100g(f) for s, f in foods.items()})
    original = recipes_repo.compute_nutrition(recipe).per_serving
    variant = RecipeVariant(
        base_recipe_id=recipe.id,
        user_id=user_id,
        label=save.label,
        targets=target.model_dump(mode="json"),
        ingredient_changes=[line.to_json() for line in lines],
        nutrition=_nutrition_json(per_serving, original, target),
        explanations=[_explanation_json(e) for e in explanations],
    )
    session.add(variant)
    await session.flush()
    if save.plan_id is not None and save.slot is not None:
        plan = await slots.owned_plan(session, user_id, save.plan_id)
        slot = slots.find_slot(plan, save.slot)
        if slot.recipe_id != recipe.id:
            raise HTTPException(status.HTTP_409_CONFLICT, "the slot has another recipe")
        if slot.status in slots.LOCKED:
            raise HTTPException(status.HTTP_409_CONFLICT, f"the meal is already {slot.status}")
        existing = await session.get(PlanSlotVariant, slot.id)
        if existing is not None:
            existing.variant_id = variant.id
        else:
            session.add(PlanSlotVariant(slot_id=slot.id, variant_id=variant.id))
        _cook_from(slot, lines, per_serving)
    return variant


def _cook_from(slot: PlanSlot, lines: Sequence[VariantLine], per_serving: Nutrients) -> None:
    slots.set_nutrition(slot, per_serving.scale(slot.portion))
    slot.leave_out = [line.key for line in lines if line.removed]


async def owned(
    session: AsyncSession, user_id: uuid.UUID, variant_id: uuid.UUID, lock: bool = True
) -> RecipeVariant:
    stmt = select(RecipeVariant).where(
        RecipeVariant.id == variant_id, RecipeVariant.user_id == user_id
    )
    if lock:
        stmt = stmt.with_for_update()
    variant = (await session.scalars(stmt.execution_options(populate_existing=True))).one_or_none()
    if variant is None:
        # another user's variant looks the same as a missing one
        raise HTTPException(status.HTTP_404_NOT_FOUND, "variant not found")
    return variant


async def variant_out(session: AsyncSession, variant: RecipeVariant) -> VariantOut:
    lines = [VariantLine.from_json(d) for d in variant.ingredient_changes]
    foods = await foods_repo.get_by_slugs(session, [line.food for line in lines])
    linked = await session.execute(
        select(PlanSlot.plan_id, PlanSlot.position)
        .join(PlanSlotVariant, PlanSlotVariant.slot_id == PlanSlot.id)
        .where(PlanSlotVariant.variant_id == variant.id)
        .order_by(PlanSlot.plan_id, PlanSlot.position)
    )
    n = variant.nutrition
    return VariantOut(
        id=variant.id,
        recipe_id=variant.base_recipe_id,
        label=variant.label,
        target=MealTarget.model_validate(variant.targets),
        lines=[
            VariantLineOut(
                key=line.key,
                position=line.position,
                food=FoodRef(
                    slug=line.food,
                    name_en=foods[line.food].name_en,
                    name_pl=foods[line.food].name_pl,
                ),
                original_food=line.original_food,
                original_g=line.original_g,
                grams=line.grams,
                culinary_role=line.role,
                optional=line.optional,
                removed=line.removed,
                swapped=line.swapped,
            )
            for line in lines
        ],
        original_nutrition=nutrients_out(Nutrients(**n["original"])),
        nutrition=nutrients_out(Nutrients(**n["per_serving"])),
        on_target=n["on_target"],
        misses=[MissOut.model_validate(m) for m in n["misses"]],
        explanations=[ExplanationOut.model_validate(e) for e in variant.explanations],
        plan_slots=[SlotRefOut(plan_id=p, slot=s) for p, s in linked.all()],
        created_at=variant.created_at,
    )


async def substitute(
    session: AsyncSession, user_id: uuid.UUID, variant_id: uuid.UUID, body: SubstituteIn
) -> SubstituteOut:
    """Swap one ingredient, or handle "I don't have this", and update the plan slots using it.

    Substitutes come from the Substitution Engine with the user's exclusions,
    so an excluded food is never offered; the resulting lines are checked once
    more before anything is saved. Day rebalances are returned as proposals.
    """
    variant = await owned(session, user_id, variant_id)
    excl = await exclusions(session, user_id, body.exclusions)
    lines = [VariantLine.from_json(d) for d in variant.ingredient_changes]
    line = next((x for x in lines if x.key == body.ingredient and not x.removed), None)
    if line is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "ingredient not found")
    foods = await foods_repo.get_by_slugs(session, [x.food for x in lines])
    food = foods[line.food]

    recipe = await recipes_repo.get(session, variant.base_recipe_id)
    assert recipe is not None  # variants cascade with their recipe
    fix = None
    if not line.swapped:
        fixes = await recipes_repo.propose_fixes(session, recipe, excl)
        fix = next((f for f in fixes if f.key == line.key), None)
    missing = body.food is None
    leave_out = missing and (line.optional or (fix is not None and fix.remove))

    if leave_out or line.grams <= 0:
        if not line.optional:
            raise HTTPException(status.HTTP_409_CONFLICT, "no safe substitute found")
        new_lines = vlines.leave_out(lines, line.key)
        change = explain.left_out(
            line.key,
            food.name_en,
            line.grams,
            for_grams(_per_100g(food), line.grams).scale(-1),
            missing=missing,
        )
    else:
        candidates = await foods_repo.substitution_candidates(session, food, line.role.value)
        by_slug = {c.slug: c for c in candidates}
        ranked = options(
            to_substitution_food(food),
            line.grams,
            line.role,
            [to_substitution_food(c) for c in candidates],
            excl,
            limit=MAX_OPTIONS,
        )
        option = vlines.choose(ranked, body.food)
        if option is None:
            if missing:
                raise HTTPException(status.HTTP_409_CONFLICT, "no safe substitute found")
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT, "not a safe substitute for this ingredient"
            )
        new_lines = vlines.substitute(lines, line.key, option)
        new = by_slug[option.key]
        foods[new.slug] = new
        grams = next(x.grams for x in new_lines if x.key == line.key)
        change = explain.swap(
            line.key,
            food.name_en,
            line.grams,
            new.name_en,
            grams,
            line.role,
            _diff(food, line.grams, new, grams),
            missing=missing,
        )

    allergens = {s: to_allergens(f) for s, f in foods.items()}
    conflicts = vlines.conflicts(new_lines, allergens, excl)
    if line.key in conflicts:  # the engine never offers an excluded food; never save one
        raise HTTPException(status.HTTP_409_CONFLICT, "no safe substitute found")

    per_100g = {s: _per_100g(f) for s, f in foods.items()}
    before = vlines.nutrition(lines, per_100g)
    after = vlines.nutrition(new_lines, per_100g)
    target = MealTarget.model_validate(variant.targets)
    original = Nutrients(**variant.nutrition["original"])
    variant.ingredient_changes = [x.to_json() for x in new_lines]
    variant.nutrition = _nutrition_json(after, original, target)
    variant.explanations = [*variant.explanations, _explanation_json(change)]

    rebalances = []
    for plan, days in await _plans_using(session, user_id, variant):
        for slot in plan.slots:
            if slot.day in days and slot.position in days[slot.day]:
                _cook_from(slot, new_lines, after)
        for day in sorted(days):
            proposal = slots.proposal(plan, day, days[day])
            if proposal.needed or not proposal.within_tolerance:
                rebalances.append(proposal)
    await session.flush()

    return SubstituteOut(
        variant=await variant_out(session, variant),
        change=explanation_out(change),
        previous_nutrition=nutrients_out(before),
        nutrition=nutrients_out(after),
        delta=nutrients_out(after + before.scale(-1)),
        conflicts=[k for k in conflicts if k != line.key],
        rebalance=rebalances,
    )


async def _plans_using(
    session: AsyncSession, user_id: uuid.UUID, variant: RecipeVariant
) -> list[tuple[MealPlan, dict[int, set[int]]]]:
    """The user's plans with slots cooked from the variant: day → positions, not locked."""
    rows = await session.execute(
        select(PlanSlot.plan_id, PlanSlot.day, PlanSlot.position)
        .join(PlanSlotVariant, PlanSlotVariant.slot_id == PlanSlot.id)
        .where(PlanSlotVariant.variant_id == variant.id, PlanSlot.status.not_in(slots.LOCKED))
        .order_by(PlanSlot.plan_id)
    )
    by_plan: dict[uuid.UUID, dict[int, set[int]]] = {}
    for plan_id, day, position in rows.all():
        by_plan.setdefault(plan_id, {}).setdefault(day, set()).add(position)
    return [
        (await slots.owned_plan(session, user_id, plan_id), days)
        for plan_id, days in by_plan.items()
    ]
