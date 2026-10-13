"""Planner v1 on small synthetic inputs: filter, score, CP-SAT assignment, reports."""

from __future__ import annotations

import dataclasses
from collections.abc import Iterable

import pytest

from app.nutrition.allergens import (
    Allergen,
    Exclusion,
    ExclusionCategory,
    IngredientAllergens,
    Origin,
    Severity,
    TraceStatus,
)
from app.nutrition.nutrients import Nutrients
from app.planner.filter import Reason, screen
from app.planner.inputs import Candidate, MealSlot, MealType, Profile
from app.planner.plan import plan, verify
from app.planner.result import Action, BlockerKind, Infeasible, Plan
from app.planner.score import score
from app.planner.solve import MAX_COOKS, Rule, SolverConfig, Status
from app.recipes.safety import CheckLine

CONFIG = SolverConfig(deterministic_time=1.0, time_limit_s=30.0, workers=1, seed=0)
BREAKFAST = MealSlot("breakfast", MealType.BREAKFAST, 0.4)
DINNER = MealSlot("dinner", MealType.DINNER, 0.6)
SAFE = IngredientAllergens(Origin.PLANT, trace_status=TraceStatus.NONE_DECLARED)
MILK = IngredientAllergens(
    Origin.DAIRY, frozenset({Allergen.MILK}), trace_status=TraceStatus.NONE_DECLARED
)


def line(key: str, allergens: IngredientAllergens = SAFE, optional: bool = False) -> CheckLine:
    return CheckLine(key, allergens, optional)


def recipe(
    id: str,
    tags: Iterable[str] = ("dinner",),
    kcal: float = 600,
    protein: float = 40,
    fridge_days: int = 0,
    prep_score: int = 0,
    minutes: int = 20,
    equipment: Iterable[str] = (),
    lines: tuple[CheckLine, ...] | None = None,
    ingredients: Iterable[str] = (),
) -> Candidate:
    return Candidate(
        id=id,
        tags=frozenset(tags),
        per_serving=Nutrients(kcal=kcal, protein_g=protein),
        servings=2,
        fridge_days=fridge_days,
        freezer_friendly=False,
        meal_prep_score=prep_score,
        total_minutes=minutes,
        equipment=frozenset(equipment),
        allergen_lines=lines if lines is not None else (line(f"0:{id}"),),
        ingredient_ids=frozenset(ingredients),
    )


def profile(**changes: object) -> Profile:
    base = Profile(
        daily_kcal=2000,
        protein_min_g=100,
        meals=(BREAKFAST, DINNER),
        days=3,
    )
    return dataclasses.replace(base, **changes)  # type: ignore[arg-type]


def menu(n_breakfasts: int = 4, n_dinners: int = 4, **kw: object) -> list[Candidate]:
    breakfasts = [
        recipe(f"b{i}", ("breakfast",), kcal=700 + 20 * i, protein=40, **kw)  # type: ignore[arg-type]
        for i in range(n_breakfasts)
    ]
    dinners = [
        recipe(f"d{i}", ("dinner",), kcal=1100 + 20 * i, protein=60, **kw)  # type: ignore[arg-type]
        for i in range(n_dinners)
    ]
    return breakfasts + dinners


def solved(candidates: list[Candidate], p: Profile) -> Plan:
    result = plan(candidates, p, CONFIG)
    assert isinstance(result, Plan), result.message
    assert verify(result, candidates, p) == []
    return result


def infeasible(candidates: list[Candidate], p: Profile) -> Infeasible:
    result = plan(candidates, p, CONFIG)
    assert isinstance(result, Infeasible)
    return result


# ── profile ──────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "changes",
    [
        {"daily_kcal": 1199},
        {"days": 4},
        {"prep_days": 4},
        {"prep_days": 0},
        {"meals": (BREAKFAST,)},
        {"meals": (BREAKFAST, dataclasses.replace(DINNER, kcal_share=0.5))},
        {"meals": (BREAKFAST, dataclasses.replace(DINNER, name="breakfast"))},
        {"protein_min_g": -1},
        {"max_minutes": 0},
    ],
)
def test_profile_rejects_invalid_settings(changes: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        profile(**changes)


def test_kcal_window_never_goes_below_the_floor() -> None:
    assert profile(daily_kcal=1200).kcal_window == (1200, 1260)
    assert profile(daily_kcal=2000).kcal_window == (1900, 2100)


# ── filter ───────────────────────────────────────────────────────────────


def test_allergy_blocks_a_required_ingredient() -> None:
    c = recipe("r", lines=(line("0:pasta"), line("1:cheese", MILK)))
    s = screen(c, profile(exclusions=(Exclusion(ExclusionCategory.MILK, Severity.ALLERGY),)))
    assert s.reasons == {Reason.EXCLUSION}
    assert [e.category for e in s.blocked_by] == [ExclusionCategory.MILK]


def test_excluded_optional_ingredient_is_left_out() -> None:
    c = recipe("r", lines=(line("0:pasta"), line("1:cheese", MILK, optional=True)))
    s = screen(c, profile(exclusions=(Exclusion(ExclusionCategory.MILK, Severity.ALLERGY),)))
    assert s.allowed
    assert s.leave_out == ("1:cheese",)


def test_allergy_blocks_unknown_traces_but_intolerance_does_not() -> None:
    unknown = IngredientAllergens(Origin.PLANT)  # trace status defaults to unknown
    c = recipe("r", lines=(line("0:bread", unknown),))
    allergy = Exclusion(ExclusionCategory.MILK, Severity.ALLERGY)
    intolerance = Exclusion(ExclusionCategory.MILK, Severity.INTOLERANCE)
    assert not screen(c, profile(exclusions=(allergy,))).allowed
    assert screen(c, profile(exclusions=(intolerance,))).allowed


def test_relaxed_intolerance_is_penalised_and_labelled() -> None:
    c = recipe("r", lines=(line("0:cheese", MILK),))
    relaxed = Exclusion(ExclusionCategory.MILK, Severity.INTOLERANCE, relaxed=True)
    s = screen(c, profile(exclusions=(relaxed,)))
    assert s.allowed
    assert [p.exclusion for p in s.penalties] == [relaxed]


def test_recipe_without_ingredient_data_is_blocked_only_by_hard_exclusions() -> None:
    c = recipe("r", lines=())
    assert screen(c, profile()).allowed
    dislike = Exclusion(ExclusionCategory.MILK, Severity.DISLIKE)
    assert screen(c, profile(exclusions=(dislike,))).allowed
    allergy = Exclusion(ExclusionCategory.FISH, Severity.ALLERGY)
    assert screen(c, profile(exclusions=(allergy,))).reasons == {Reason.UNCHECKED}


def test_time_and_equipment() -> None:
    c = recipe("r", minutes=40, equipment=("pot", "oven"))
    s = screen(c, profile(max_minutes=30))
    assert s.reasons == {Reason.TIME, Reason.EQUIPMENT}
    assert s.missing_equipment == {"oven"}
    assert screen(c, profile(max_minutes=45, equipment=frozenset({"oven"}))).allowed


# ── score ────────────────────────────────────────────────────────────────


def test_dislike_scores_below_prefer_not() -> None:
    c = recipe("r", lines=(line("0:cheese", MILK),))
    scores = {}
    for severity in (Severity.DISLIKE, Severity.PREFER_NOT):
        p = profile(exclusions=(Exclusion(ExclusionCategory.MILK, severity),))
        scores[severity] = score(screen(c, p), DINNER, p).total
    assert scores[Severity.DISLIKE] < scores[Severity.PREFER_NOT]


def test_meal_prep_counts_only_when_batching() -> None:
    c = recipe("r", prep_score=100, fridge_days=3)
    assert score(screen(c, profile()), DINNER, profile()).meal_prep == 0
    p = profile(prep_days=3)
    assert score(screen(c, p), DINNER, p).meal_prep > 0


def test_protein_dense_recipe_scores_higher() -> None:
    p = profile()
    lean = score(screen(recipe("a", protein=60), p), DINNER, p)
    fatty = score(screen(recipe("b", protein=10), p), DINNER, p)
    assert lean.macro > fatty.macro


# ── assignment ───────────────────────────────────────────────────────────


def test_plan_meets_daily_targets() -> None:
    p = profile(days=5)
    result = solved(menu(), p)
    for day in result.days:
        assert 1900 <= day.totals.kcal <= 2100
        assert day.totals.protein_g >= 100
        assert [m.slot for m in day.meals] == ["breakfast", "dinner"]
    assert result.notices == ()


def test_no_day_below_1200_kcal() -> None:
    small = [
        recipe("b", ("breakfast",), kcal=480, protein=30),
        recipe("b2", ("breakfast",), kcal=500, protein=30),
        recipe("d", ("dinner",), kcal=700, protein=40),
        recipe("d2", ("dinner",), kcal=740, protein=40),
    ]
    p = profile(daily_kcal=1200, protein_min_g=50)
    for day in solved(small, p).days:
        assert 1200 <= day.totals.kcal <= 1260


def test_plan_is_deterministic() -> None:
    p = profile(days=7, prep_days=2)
    candidates = menu(fridge_days=3, prep_score=80)
    assert solved(candidates, p) == solved(candidates, p)


def test_batch_never_spans_more_than_fridge_days() -> None:
    # one breakfast that keeps 2 days, cook once for 3: batches of at most 2
    candidates = [recipe("oats", ("breakfast",), kcal=800, protein=40, fridge_days=2,
                         prep_score=90), *menu(0, 4)]  # fmt: skip
    p = profile(days=7, prep_days=3)
    result = solved(candidates, p)
    run = 0
    for day in result.days:
        meal = day.meals[0]
        assert meal.recipe_id == "oats"
        run = run + 1 if meal.from_batch else 1
        assert run <= 2
        assert meal.day - meal.cook_day + 1 <= 2
        assert meal.eat_by_day >= meal.day
    # 7 breakfasts from one recipe needs 4 cooks: more than the variety limit
    assert Rule.VARIETY in result.relaxed
    assert result.notices and "oats" in result.notices[0]


def test_batch_is_eaten_in_equal_portions() -> None:
    p = profile(days=7, prep_days=3)
    result = solved(menu(fridge_days=4, prep_score=90), p)
    meals = {(m.day, m.slot): m for m in result.meals}
    batched = [m for m in result.meals if m.from_batch]
    assert batched
    for m in batched:
        before = meals[m.day - 1, m.slot]
        assert (before.recipe_id, before.portion) == (m.recipe_id, m.portion)


def test_fresh_only_recipes_are_never_batched() -> None:
    p = profile(days=5, prep_days=3)
    result = solved(menu(fridge_days=0, prep_score=90), p)
    assert not any(m.from_batch for m in result.meals)


def test_low_prep_score_recipes_are_never_batched() -> None:
    p = profile(days=5, prep_days=3)
    result = solved(menu(fridge_days=4, prep_score=10), p)
    assert not any(m.from_batch for m in result.meals)


def test_variety_limit_holds_when_there_is_choice() -> None:
    result = solved(menu(6, 6), profile(days=7))
    cooks: dict[str, int] = {}
    for m in result.meals:
        cooks[m.recipe_id] = cooks.get(m.recipe_id, 0) + 1
    assert max(cooks.values()) <= MAX_COOKS


def test_recipe_used_once_a_day_even_if_it_fits_two_slots() -> None:
    both = [recipe(f"x{i}", ("breakfast", "dinner"), kcal=1000, protein=60) for i in range(3)]
    result = solved(both, profile(days=3, meals=(
        dataclasses.replace(BREAKFAST, kcal_share=0.5), dataclasses.replace(DINNER, kcal_share=0.5)
    )))  # fmt: skip
    for day in result.days:
        assert len({m.recipe_id for m in day.meals}) == 2


def test_ingredient_reuse_prefers_shared_ingredients() -> None:
    shared = ("oats", "milk")
    candidates = [
        recipe("b-shared", ("breakfast",), kcal=800, protein=50, ingredients=shared),
        recipe("b-other", ("breakfast",), kcal=800, protein=50, ingredients=("rye", "kefir")),
        recipe("d-shared", ("dinner",), kcal=1200, protein=60, ingredients=shared),
        recipe("d-other", ("dinner",), kcal=1200, protein=60, ingredients=("rice", "tofu")),
    ]
    result = solved(candidates, profile(days=3))
    used = {m.recipe_id for m in result.meals}
    assert {"b-shared", "d-shared"} <= used


def test_disliked_recipe_is_avoided_when_there_is_an_alternative() -> None:
    candidates = [*menu(2, 0), recipe("d-cheese", lines=(line("0:cheese", MILK),), kcal=1150,
                  protein=60), recipe("d-plain", kcal=1150, protein=60),
                  recipe("d-plain2", kcal=1170, protein=60)]  # fmt: skip
    p = profile(exclusions=(Exclusion(ExclusionCategory.MILK, Severity.DISLIKE),))
    result = solved(candidates, p)
    assert "d-cheese" not in {m.recipe_id for m in result.meals}


def test_relaxed_intolerance_is_labelled_when_used() -> None:
    candidates = [*menu(2, 0), recipe("d-cheese", lines=(line("0:cheese", MILK),), kcal=1150,
                  protein=60)]  # fmt: skip
    relaxed = Exclusion(ExclusionCategory.MILK, Severity.INTOLERANCE, relaxed=True)
    result = solved(candidates, profile(exclusions=(relaxed,)))
    dinners = [m for m in result.meals if m.slot == "dinner"]
    assert all("avoid when possible" in m.labels[0] for m in dinners)


def test_duplicate_ids_are_rejected() -> None:
    with pytest.raises(ValueError):
        plan([recipe("a"), recipe("a")], profile(), CONFIG)


# ── infeasible ───────────────────────────────────────────────────────────


def test_no_candidates_reports_each_slot() -> None:
    report = infeasible([], profile())
    assert [b.kind for b in report.blockers] == [BlockerKind.NO_RECIPES] * 2
    assert {s.value for s in report.suggestions} == {MealType.BREAKFAST, MealType.DINNER}
    assert "There are no breakfasts to choose from." in report.message


def test_time_limit_report_names_the_limit_and_the_fix() -> None:
    candidates = [*menu(2, 0), *menu(0, 3, minutes=40)]
    report = infeasible(candidates, profile(max_minutes=20))
    assert report.blockers[0].message == "No dinners match the 20-minute limit."
    assert report.blockers[0].meal == "dinner"
    fix = next(s for s in report.suggestions if s.action is Action.MAX_MINUTES)
    assert fix.value == 45
    assert fix.message == "Raise your max cooking time to 45 minutes"


def test_equipment_report_suggests_the_missing_appliance() -> None:
    candidates = [*menu(2, 0), *menu(0, 3, equipment=("oven",))]
    report = infeasible(candidates, profile())
    assert "your equipment (no oven)" in report.blockers[0].message
    assert any(s.action is Action.ADD_EQUIPMENT and s.value == "oven" for s in report.suggestions)


def test_intolerance_can_be_relaxed_but_allergy_never() -> None:
    cheesy = (line("0:cheese", MILK),)
    candidates = [*menu(2, 0), *menu(0, 3, lines=cheesy)]
    intolerance = Exclusion(ExclusionCategory.MILK, Severity.INTOLERANCE)
    report = infeasible(candidates, profile(exclusions=(intolerance,)))
    assert report.blockers[0].message == "No dinners match your exclusions (milk)."
    assert any(s.action is Action.RELAX_INTOLERANCE for s in report.suggestions)

    allergy = Exclusion(ExclusionCategory.MILK, Severity.ALLERGY)
    report = infeasible(candidates, profile(exclusions=(allergy,)))
    assert not any(s.action is Action.RELAX_INTOLERANCE for s in report.suggestions)


def test_protein_minimum_is_never_dropped() -> None:
    report = infeasible(menu(), profile(protein_min_g=250))
    assert report.blockers[0].kind is BlockerKind.PROTEIN
    assert "250 g protein" in report.blockers[0].message
    assert any(s.action is Action.LOWER_PROTEIN for s in report.suggestions)


def test_unreachable_calories_say_how_far_off() -> None:
    tiny = [recipe(f"b{i}", ("breakfast",), kcal=150, protein=20) for i in range(3)] + [
        recipe(f"d{i}", ("dinner",), kcal=200, protein=30) for i in range(3)
    ]
    report = infeasible(tiny, profile(protein_min_g=0))
    assert report.blockers[0].kind is BlockerKind.KCAL
    assert "protein" not in report.blockers[0].message
    assert "largest portions add up to only about 700 kcal" in report.blockers[0].message
    assert any(s.action is Action.CHANGE_KCAL for s in report.suggestions)


def test_timeout_is_reported_not_raised() -> None:
    tight = SolverConfig(deterministic_time=0.0, time_limit_s=0.0)
    result = plan(menu(6, 6), profile(days=7), tight)
    assert isinstance(result, Infeasible)
    assert result.status is Status.TIMEOUT
    assert result.blockers[0].kind is BlockerKind.TIMEOUT
