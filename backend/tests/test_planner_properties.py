"""Property tests: whatever the input, a plan keeps every hard constraint, and
an impossible input gives a report, never a crash.

The checks here are written independently of the planner's own ``verify``.
"""

from __future__ import annotations

import dataclasses

from hypothesis import HealthCheck, event, given, settings
from hypothesis import strategies as st

from app.nutrition.allergens import (
    Allergen,
    Exclusion,
    ExclusionCategory,
    IngredientAllergens,
    Origin,
    Severity,
    TraceStatus,
    Verdict,
    classify_all,
)
from app.nutrition.nutrients import Nutrients
from app.planner.inputs import BASIC_TOOLS, Candidate, MealSlot, MealType, Profile
from app.planner.plan import plan, verify
from app.planner.result import Infeasible, Plan
from app.planner.solve import SolverConfig
from app.recipes.safety import CheckLine

CONFIG = SolverConfig(deterministic_time=0.3, time_limit_s=10.0, workers=1, seed=0)
ALLERGENS = [Allergen.MILK, Allergen.GLUTEN, Allergen.EGGS]
MEAL_TAGS = ["breakfast", "lunch", "dinner", "snack"]

ingredient = st.builds(
    IngredientAllergens,
    origin=st.sampled_from([Origin.PLANT, Origin.DAIRY, Origin.MEAT]),
    contains=st.frozensets(st.sampled_from(ALLERGENS), max_size=2),
    may_contain=st.frozensets(st.sampled_from(ALLERGENS), max_size=1),
    trace_status=st.sampled_from(list(TraceStatus)),
)


@st.composite
def candidates(draw: st.DrawFn) -> list[Candidate]:
    n = draw(st.integers(0, 10))
    result = []
    for i in range(n):
        lines = draw(st.lists(ingredient, max_size=3))
        result.append(
            Candidate(
                id=f"r{i}",
                tags=frozenset(draw(st.lists(st.sampled_from(MEAL_TAGS), min_size=1, max_size=2))),
                per_serving=Nutrients(
                    kcal=draw(st.floats(80, 1200).map(lambda v: round(v, 1))),
                    protein_g=draw(st.floats(0, 80).map(lambda v: round(v, 1))),
                ),
                servings=draw(st.integers(1, 6)),
                fridge_days=draw(st.integers(0, 5)),
                freezer_friendly=draw(st.booleans()),
                meal_prep_score=draw(st.integers(0, 100)),
                total_minutes=draw(st.integers(1, 90)),
                equipment=frozenset(draw(st.lists(st.sampled_from(["pot", "oven", "blender"])))),
                allergen_lines=tuple(
                    CheckLine(f"{j}:food", a, draw(st.booleans())) for j, a in enumerate(lines)
                ),
            )
        )
    return result


SHARES = {
    2: (0.45, 0.55),
    3: (0.3, 0.35, 0.35),
    4: (0.25, 0.3, 0.3, 0.15),
}
SLOT_TYPES = {
    2: (MealType.BREAKFAST, MealType.DINNER),
    3: (MealType.BREAKFAST, MealType.LUNCH, MealType.DINNER),
    4: (MealType.BREAKFAST, MealType.LUNCH, MealType.DINNER, MealType.SNACK),
}


@st.composite
def profiles(draw: st.DrawFn) -> Profile:
    n = draw(st.sampled_from([2, 3, 4]))
    meals = tuple(
        MealSlot(t.value, t, share) for t, share in zip(SLOT_TYPES[n], SHARES[n], strict=True)
    )
    exclusions = draw(
        st.lists(
            st.builds(
                Exclusion,
                category=st.sampled_from(
                    [ExclusionCategory.MILK, ExclusionCategory.GLUTEN, ExclusionCategory.MEAT]
                ),
                severity=st.sampled_from(list(Severity)),
            ),
            max_size=2,
            unique_by=lambda e: e.category,
        )
    )
    return Profile(
        daily_kcal=draw(st.integers(1200, 3200)),
        protein_min_g=draw(st.integers(0, 180)),
        meals=meals,
        days=draw(st.sampled_from([3, 5])),
        prep_days=draw(st.integers(1, 3)),
        max_minutes=draw(st.sampled_from([15, 30, 45, 60, None])),
        equipment=frozenset(draw(st.lists(st.sampled_from(["oven", "blender"])))),
        exclusions=tuple(exclusions),
    )


def _check_hard_constraints(result: Plan, cands: list[Candidate], profile: Profile) -> None:
    by_id = {c.id: c for c in cands}
    hard = profile.hard_exclusions
    lo, hi = profile.kcal_window
    slot_types = {m.name: m.meal_type for m in profile.meals}
    assert len(result.days) == profile.days
    for day in result.days:
        assert len(day.meals) == len(profile.meals)
        assert lo - 1e-6 <= day.totals.kcal <= hi + 1e-6
        assert day.totals.kcal >= 1200 - 1e-6
        assert day.totals.protein_g >= profile.protein_min_g - 1e-6
        for meal in day.meals:
            c = by_id[meal.recipe_id]
            assert c.fits(slot_types[meal.slot])
            if profile.max_minutes is not None:
                assert c.total_minutes <= profile.max_minutes
            assert c.equipment - BASIC_TOOLS <= profile.equipment
            if hard:
                assert c.allergen_lines, "unchecked recipe planned for a hard exclusion"
            for line in c.allergen_lines:
                if classify_all(line.allergens, hard) is Verdict.EXCLUDED:
                    assert line.optional and line.key in meal.leave_out
            # a batch never spans more days than the recipe keeps, or than N
            span = meal.day - meal.cook_day + 1
            if meal.from_batch:
                assert span <= max(1, c.fridge_days)
                assert span <= profile.prep_days
            else:
                assert meal.cook_day == meal.day


@settings(
    max_examples=60,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.data_too_large],
)
@given(cands=candidates(), profile=profiles())
def test_plan_keeps_hard_constraints_or_reports(cands: list[Candidate], profile: Profile) -> None:
    result = plan(cands, profile, CONFIG)
    event(type(result).__name__)
    if isinstance(result, Plan):
        _check_hard_constraints(result, cands, profile)
        assert verify(result, cands, profile) == []
    else:
        assert isinstance(result, Infeasible)
        assert result.blockers
        assert all(b.message for b in result.blockers)
        assert result.suggestions
        # never offer to relax an allergy
        allergies = {e.category.value for e in profile.exclusions if e.severity is Severity.ALLERGY}
        assert not any(s.value in allergies for s in result.suggestions if s.value)


@settings(max_examples=25, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(
    kcal=st.lists(st.floats(300, 900).map(lambda v: round(v, 1)), min_size=2, max_size=6),
    fridge=st.integers(0, 4),
    prep_days=st.integers(1, 3),
)
def test_batches_never_exceed_fridge_days(kcal: list[float], fridge: int, prep_days: int) -> None:
    # plenty of feasible choices, all batchable: stress the meal-prep grouping
    cands = [
        Candidate(
            id=f"{t}{i}",
            tags=frozenset({t}),
            per_serving=Nutrients(kcal=k, protein_g=k / 10),
            servings=4,
            fridge_days=fridge,
            freezer_friendly=False,
            meal_prep_score=90,
            total_minutes=20,
            equipment=frozenset(),
            allergen_lines=(),
        )
        for t in ("breakfast", "dinner")
        for i, k in enumerate(kcal)
    ]
    profile = Profile(
        daily_kcal=1800,
        protein_min_g=0,
        meals=(
            MealSlot("breakfast", MealType.BREAKFAST, 0.4),
            MealSlot("dinner", MealType.DINNER, 0.6),
        ),
        days=7,
        prep_days=prep_days,
    )
    result = plan(cands, profile, CONFIG)
    event(type(result).__name__)
    if isinstance(result, Infeasible):
        assert result.blockers
        return
    _check_hard_constraints(result, cands, profile)
    for m in result.meals:
        assert m.day - m.cook_day + 1 <= max(1, min(fridge, prep_days))


SAFE = IngredientAllergens(Origin.PLANT, trace_status=TraceStatus.NONE_DECLARED)


@st.composite
def plausible(draw: st.DrawFn) -> tuple[list[Candidate], Profile]:
    """Recipes sized around the profile's meals, so most inputs have a plan."""
    profile = draw(profiles())
    protein = round(profile.daily_kcal * draw(st.floats(0, 0.06)))
    profile = dataclasses.replace(profile, protein_min_g=protein)
    cands = []
    for slot in profile.meals:
        target = profile.daily_kcal * slot.kcal_share
        for i in range(draw(st.integers(1, 6))):
            kcal = round(target * draw(st.floats(0.6, 1.5)), 1)
            lines = draw(st.lists(st.one_of(st.just(SAFE), st.just(SAFE), ingredient), max_size=2))
            cands.append(
                Candidate(
                    id=f"{slot.name}{i}",
                    tags=frozenset({slot.meal_type.value}),
                    per_serving=Nutrients(
                        kcal=kcal, protein_g=round(kcal * draw(st.floats(0.02, 0.12)), 1)
                    ),
                    servings=draw(st.integers(1, 6)),
                    fridge_days=draw(st.integers(0, 5)),
                    freezer_friendly=False,
                    meal_prep_score=draw(st.integers(0, 100)),
                    total_minutes=draw(st.integers(5, 20)),
                    equipment=frozenset(draw(st.sampled_from([(), ("pot",), ("pot", "oven")]))),
                    allergen_lines=tuple(
                        CheckLine(f"{j}:food", a, draw(st.booleans())) for j, a in enumerate(lines)
                    ),
                )
            )
    return cands, profile


@settings(
    max_examples=60,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.data_too_large],
)
@given(scenario=plausible())
def test_plausible_inputs_keep_hard_constraints(
    scenario: tuple[list[Candidate], Profile],
) -> None:
    cands, profile = scenario
    result = plan(cands, profile, CONFIG)
    event(type(result).__name__)
    if isinstance(result, Infeasible):
        event(result.blockers[0].kind.value)
    if isinstance(result, Plan):
        _check_hard_constraints(result, cands, profile)
    else:
        assert result.blockers and result.suggestions
