"""Transformation engine. Nutrition values are plausible test data, not reference data."""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from app.foods.vocab import CulinaryRole as R
from app.nutrition.nutrients import Nutrients
from app.optimizer.transform import (
    KCAL_TOLERANCE_ROUNDED,
    Line,
    Metric,
    Reason,
    Target,
    bounds,
    misses,
    nutrition,
    transform,
)

CHICKEN = Nutrients(120, 22.5, 2.6, 0, 0)
RICE = Nutrients(360, 6.6, 0.6, 79, 1.3)
OIL = Nutrients(884, 0, 100, 0, 0)
BROCCOLI = Nutrients(34, 2.8, 0.4, 4.4, 2.6)
EGG = Nutrients(143, 12.6, 9.5, 0.7, 0)
CHEESE = Nutrients(300, 24, 20, 3, 0)
SALT = Nutrients(0, 0, 0, 0, 0)


def bowl() -> list[Line]:
    return [
        Line("chicken", CHICKEN, 150, R.MAIN_PROTEIN),
        Line("rice", RICE, 80, R.CARB_BASE),
        Line("oil", OIL, 15, R.COOKING_FAT),
        Line("broccoli", BROCCOLI, 150, R.VEGETABLE),
        Line("salt", SALT, 1, R.SEASONING),
    ]


def test_cuts_calories_and_keeps_protein() -> None:
    lines = bowl()
    before = nutrition(lines, {ln.key: ln.grams for ln in lines})
    assert before.kcal > 600
    result = transform(lines, Target(kcal=480, protein_min_g=38))

    assert result.on_target, result.misses
    assert result.nutrition.kcal == pytest.approx(480, rel=KCAL_TOLERANCE_ROUNDED)
    assert result.nutrition.protein_g >= 38
    assert result.grams["salt"] == 1
    assert result.grams["oil"] < 15
    assert {c.key for c in result.changes} >= {"oil"}
    oil = next(c for c in result.changes if c.key == "oil")
    assert oil.reason in (Reason.CUT_CALORIES, Reason.LOWER_FAT)


def test_raises_protein_with_the_protein_ingredient() -> None:
    lines = bowl()
    result = transform(lines, Target(kcal=640, protein_min_g=50))
    assert result.on_target, result.misses
    chicken = next(c for c in result.changes if c.key == "chicken")
    assert chicken.grams > 150
    assert chicken.reason is Reason.RAISE_PROTEIN


def test_unreachable_target_is_reported_not_hidden() -> None:
    result = transform(bowl(), Target(kcal=150, protein_min_g=60))
    assert not result.on_target
    assert {m.metric for m in result.misses} <= {Metric.KCAL, Metric.PROTEIN}
    assert result.misses
    for line in bowl():
        lo, hi = bounds(line)
        assert lo - 1e-6 <= result.grams[line.key] <= hi + 1e-6


def test_locked_line_is_not_changed() -> None:
    lines = [*bowl()[:2], Line("oil", OIL, 15, R.COOKING_FAT, locked=True), *bowl()[3:]]
    result = transform(lines, Target(kcal=520, protein_min_g=35))
    assert result.grams["oil"] == 15
    assert "oil" not in {c.key for c in result.changes}


def test_optional_line_may_be_removed() -> None:
    lines = [*bowl(), Line("cheese", CHEESE, 30, R.CHEESE, optional=True)]
    result = transform(lines, Target(kcal=420, protein_min_g=35))
    assert result.on_target, result.misses
    assert bounds(lines[-1])[0] == 0


def test_pieces_round_to_whole_eggs() -> None:
    lines = [
        Line("egg", EGG, 150, R.MAIN_PROTEIN, piece_g=50),
        Line("bread", RICE, 60, R.CARB_BASE),
        Line("butter", OIL, 8, R.COOKING_FAT),
    ]
    result = transform(lines, Target(kcal=420, protein_min_g=22))
    assert result.grams["egg"] % 50 == pytest.approx(0)


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        transform([], Target(500, 30))
    with pytest.raises(ValueError):
        transform(bowl(), Target(0, 30))
    with pytest.raises(ValueError):
        transform([*bowl(), bowl()[0]], Target(500, 30))


# ── Properties ────────────────────────────────────────────────────────────────


@settings(max_examples=60, deadline=None)
@given(
    kcal_factor=st.floats(0.5, 1.4),
    protein_factor=st.floats(0.5, 1.4),
    fat=st.none() | st.floats(5, 40),
    carbs=st.none() | st.floats(20, 120),
)
def test_result_is_honest_and_within_bounds(
    kcal_factor: float, protein_factor: float, fat: float | None, carbs: float | None
) -> None:
    lines = bowl()
    before = nutrition(lines, {ln.key: ln.grams for ln in lines})
    target = Target(before.kcal * kcal_factor, before.protein_g * protein_factor, fat, carbs)
    result = transform(lines, target)

    # never "on target" unless the post-rounding check passes, and misses are exact
    assert result.misses == misses(target, result.nutrition, KCAL_TOLERANCE_ROUNDED)
    assert result.on_target == (not result.misses)
    assert result.nutrition == nutrition(lines, result.grams)
    for line in lines:
        lo, hi = bounds(line)
        assert lo - 1e-6 <= result.grams[line.key] <= hi + 1e-6
    changed = {c.key for c in result.changes}
    for line in lines:
        assert (line.key in changed) == (abs(result.grams[line.key] - line.grams) > 0.5)


@settings(max_examples=40, deadline=None)
@given(kcal_factor=st.floats(0.8, 1.2))
def test_moderate_targets_are_reached(kcal_factor: float) -> None:
    lines = bowl()
    before = nutrition(lines, {ln.key: ln.grams for ln in lines})
    result = transform(lines, Target(before.kcal * kcal_factor, before.protein_g * 0.9))
    assert result.on_target, result.misses
