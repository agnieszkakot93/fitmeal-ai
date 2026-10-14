"""Daily rebalance (PRD §8.6), explanations and variant lines: pure functions."""

from __future__ import annotations

import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

from app.foods.vocab import CulinaryRole
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
from app.optimizer.substitute import Option
from app.optimizer.transform import Reason
from app.planner.inputs import KCAL_FLOOR
from app.variants import explain, lines
from app.variants.rebalance import MAX_CHANGE, Meal, propose, window

TOL = 1e-6


def _meal(position: int, kcal: float, protein: float, portion: float = 1.0, **kw: bool) -> Meal:
    n = Nutrients(kcal=kcal, protein_g=protein, fat_g=kcal / 30, carbs_g=kcal / 10)
    return Meal(position, portion, n, adjustable=kw.get("adjustable", True))


def _check(meals: list[Meal], daily_kcal: float, protein_min: float) -> None:
    """Invariants every proposal keeps, feasible or not."""
    p = propose(meals, daily_kcal, protein_min)
    by_position = {m.position: m for m in meals}
    for a in p.adjustments:
        meal = by_position[a.position]
        assert meal.adjustable
        assert abs(a.portion_to / a.portion_from - 1) <= MAX_CHANGE + 0.01
        assert a.portion_from == meal.portion
    total = Nutrients.total([m.nutrition for m in meals] + [a.delta for a in p.adjustments])
    assert abs(total.kcal - p.after.kcal) < 1e-6
    # never brings a day below the floor
    if p.before.kcal >= KCAL_FLOOR:
        assert p.after.kcal >= KCAL_FLOOR - TOL
    lo, hi = window(daily_kcal)
    if p.within_tolerance:
        assert lo - TOL <= p.after.kcal <= hi + TOL
        assert p.after.protein_g >= protein_min - TOL


def test_a_day_within_tolerance_needs_nothing() -> None:
    meals = [_meal(0, 600, 40), _meal(1, 700, 45), _meal(2, 700, 45)]
    p = propose(meals, 2000, 120)
    assert not p.needed and p.within_tolerance and p.adjustments == []
    assert p.kcal_off == 0


def test_an_over_day_trims_the_other_meals() -> None:
    # the swapped meal (fixed) is 300 kcal bigger than planned
    meals = [_meal(0, 900, 50, adjustable=False), _meal(1, 700, 45), _meal(2, 700, 45)]
    p = propose(meals, 2000, 120)
    assert p.needed and p.within_tolerance
    assert {a.position for a in p.adjustments} <= {1, 2}
    assert all(a.portion_to < a.portion_from for a in p.adjustments)
    assert 1900 <= p.after.kcal <= 2100
    _check(meals, 2000, 120)


def test_locked_meals_never_move() -> None:
    meals = [_meal(0, 400, 20, adjustable=False), _meal(1, 700, 45, adjustable=False),
             _meal(2, 600, 40)]  # fmt: skip
    p = propose(meals, 2000, 100)
    assert [a.position for a in p.adjustments] == [2]
    assert p.adjustments[0].portion_to == pytest.approx(1.2, abs=0.011)


def test_out_of_reach_says_how_far() -> None:
    # +20% on the only movable meal can't fill a 900 kcal gap
    meals = [_meal(0, 500, 30, adjustable=False), _meal(1, 600, 40)]
    p = propose(meals, 2000, 60)
    assert not p.within_tolerance
    assert p.kcal_off < 0
    assert p.after.kcal == pytest.approx(500 + 720, abs=8)
    assert round(p.kcal_off) == round(p.after.kcal - 1900)


def test_protein_minimum_is_restored() -> None:
    meals = [_meal(0, 700, 10, adjustable=False), _meal(1, 650, 60), _meal(2, 650, 30)]
    p = propose(meals, 2000, 105)
    assert p.within_tolerance
    assert p.after.protein_g >= 105
    _check(meals, 2000, 105)


def test_nothing_movable_keeps_the_day() -> None:
    meals = [_meal(0, 1500, 60, adjustable=False)]
    p = propose(meals, 2000, 100)
    assert p.adjustments == [] and not p.within_tolerance and p.kcal_off < 0


@settings(max_examples=150, deadline=None)
@given(
    st.lists(
        st.tuples(
            st.floats(150, 1200),  # kcal
            st.floats(0.05, 0.12),  # protein g per kcal
            st.sampled_from([0.5, 0.75, 1.0, 1.25, 1.5, 2.0]),
            st.booleans(),
        ),
        min_size=2,
        max_size=5,
    ),
    st.floats(0.85, 1.15),
    st.floats(0.7, 1.0),
)
def test_a_reachable_target_is_reached(
    raw: list[tuple[float, float, float, bool]], scale: float, protein_share: float
) -> None:
    """Targets built from a known in-bounds solution: the proposal must land in the window."""
    meals = [
        _meal(i, kcal, kcal * density, portion, adjustable=adjustable)
        for i, (kcal, density, portion, adjustable) in enumerate(raw)
    ]
    movable = [m for m in meals if m.adjustable]
    assume(movable)
    fixed = sum(m.nutrition.kcal for m in meals if not m.adjustable)
    daily_kcal = fixed + scale * sum(m.nutrition.kcal for m in movable)
    assume(daily_kcal * 0.95 >= KCAL_FLOOR)
    protein = sum(m.nutrition.protein_g for m in meals if not m.adjustable) + scale * sum(
        m.nutrition.protein_g for m in movable
    )
    protein_min = protein * protein_share
    p = propose(meals, daily_kcal, protein_min)
    assert p.within_tolerance, p
    _check(meals, daily_kcal, protein_min)


@settings(max_examples=150, deadline=None)
@given(
    st.lists(
        st.tuples(st.floats(100, 1500), st.floats(0, 80), st.booleans()), min_size=1, max_size=5
    ),
    st.floats(1200, 4000),
    st.floats(0, 200),
)
def test_any_day_keeps_the_rules(
    raw: list[tuple[float, float, bool]], daily_kcal: float, protein_min: float
) -> None:
    meals = [_meal(i, k, p, adjustable=a) for i, (k, p, a) in enumerate(raw)]
    _check(meals, daily_kcal, protein_min)


# ── explanations ────────────────────────────────────────────────────────────


def test_amount_change_in_plain_words() -> None:
    e = explain.amount(
        "3:olive-oil", "olive oil", 10, 2, Nutrients(kcal=-72, fat_g=-8), Reason.CUT_CALORIES
    )
    assert e.kind is explain.Kind.AMOUNT
    assert e.message == "Reduced olive oil by 8 g to fit the meal's calories → saves 72 kcal"


def test_swap_says_what_job_the_substitute_does() -> None:
    e = explain.swap(
        "0:chicken",
        "chicken breast",
        150,
        "turkey breast",
        160,
        CulinaryRole.MAIN_PROTEIN,
        Nutrients(kcal=4.2, protein_g=-2.1),
    )
    assert e.message == (
        "Swapped chicken breast (150 g) for turkey breast (160 g), to match its protein "
        "→ +4 kcal, -2 g protein"
    )
    missing = explain.swap("0:x", "milk", 200, "oat drink", 200, CulinaryRole.LIQUID,
                           Nutrients(), missing=True)  # fmt: skip
    assert missing.message.startswith("You don't have milk: using 200 g oat drink instead")
    assert "same weight" in missing.message


def test_left_out_never_says_why() -> None:
    e = explain.left_out("5:walnuts", "walnuts", 15, Nutrients(kcal=-98, protein_g=-2.3))
    assert e.message == "Left out walnuts (15 g) → saves 98 kcal, -2 g protein"
    assert e.reason is None


# ── lines ───────────────────────────────────────────────────────────────────


def _allergens(*contains: Allergen) -> IngredientAllergens:
    return IngredientAllergens(Origin.PLANT, frozenset(contains), frozenset(), (),
                               TraceStatus.NONE_DECLARED)  # fmt: skip


LINES = [
    lines.VariantLine("0:tofu", 0, "tofu", "tofu", 120, 120, CulinaryRole.MAIN_PROTEIN, False),
    lines.VariantLine("1:walnuts", 1, "walnuts", "walnuts", 15, 15, CulinaryRole.TOPPING, True),
]


def _option(key: str, disliked: bool = False) -> Option:
    return Option(key, 100, True, disliked, Nutrients(), 0.0)


def test_choose_skips_dislikes_unless_asked() -> None:
    ranked = [_option("a", disliked=True), _option("b")]
    assert lines.choose(ranked, None) == ranked[1]
    assert lines.choose(ranked, "a") == ranked[0]
    assert lines.choose(ranked, "zzz") is None
    assert lines.choose([], None) is None
    assert lines.choose([ranked[0]], None) == ranked[0]


def test_round_trip_and_nutrition() -> None:
    assert [lines.VariantLine.from_json(x.to_json()) for x in LINES] == LINES
    per_100g = {"tofu": Nutrients(kcal=100, protein_g=10), "walnuts": Nutrients(kcal=650)}
    assert lines.nutrition(LINES, per_100g).kcal == pytest.approx(120 + 97.5)
    out = lines.leave_out(LINES, "1:walnuts")
    assert lines.nutrition(out, per_100g).kcal == pytest.approx(120)
    swapped = lines.substitute(LINES, "0:tofu", Option("tempeh", 90.04, True, False,
                                                       Nutrients(), 0))  # fmt: skip
    assert swapped[0].food == "tempeh" and swapped[0].grams == 90.0 and swapped[0].swapped


def test_conflicts_cover_every_line_left_in() -> None:
    allergens = {"tofu": _allergens(Allergen.SOY), "walnuts": _allergens(Allergen.TREE_NUTS)}
    nuts = [Exclusion(ExclusionCategory.TREE_NUTS, Severity.ALLERGY)]
    assert lines.conflicts(LINES, allergens, nuts) == ["1:walnuts"]
    assert lines.conflicts(lines.leave_out(LINES, "1:walnuts"), allergens, nuts) == []
    dislike = [Exclusion(ExclusionCategory.SOY, Severity.DISLIKE)]
    assert lines.conflicts(LINES, allergens, dislike) == []
