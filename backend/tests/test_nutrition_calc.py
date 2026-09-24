import pytest

from app.nutrition.calc import FoodFacts, IngredientLine, calculate
from app.nutrition.nutrients import Nutrients, energy_is_consistent, for_grams
from app.nutrition.units import FoodUnitData

CHICKEN = FoodFacts("chicken", Nutrients(120, 22.5, 2.6, 0, 0), FoodUnitData())
OIL = FoodFacts("oil", Nutrients(884, 0, 100, 0, 0), FoodUnitData(density_g_per_ml=0.91))
RICE = FoodFacts(
    "rice", Nutrients(365, 7.1, 0.7, 78.7, 1.3), FoodUnitData(portions_g={"szklanka": 200})
)


def test_for_grams_scales_per_100g() -> None:
    n = for_grams(CHICKEN.per_100g, 250)
    assert n.kcal == pytest.approx(300)
    assert n.protein_g == pytest.approx(56.25)


def test_recipe_totals_and_per_serving() -> None:
    result = calculate(
        [
            IngredientLine(CHICKEN, 400, "g"),
            IngredientLine(OIL, 1, "łyżka"),
            IngredientLine(RICE, 1, "szklanka"),
        ],
        servings=2,
    )
    oil_g = 15 * 0.91
    assert [r.grams for r in result.lines] == pytest.approx([400, oil_g, 200])
    expected_kcal = 480 + 884 * oil_g / 100 + 730
    assert result.total.kcal == pytest.approx(expected_kcal)
    assert result.per_serving.kcal == pytest.approx(expected_kcal / 2)
    assert result.per_serving.protein_g == pytest.approx((90 + 14.2) / 2)
    assert result.total_grams == pytest.approx(600 + oil_g)


def test_servings_must_be_positive() -> None:
    with pytest.raises(ValueError):
        calculate([IngredientLine(CHICKEN, 100, "g")], servings=0)


def test_rounding_for_display() -> None:
    r = Nutrients(123.6, 10.04, 3.35, 0.0, 0.0).rounded()
    assert (r.kcal, r.protein_g, r.fat_g) == (124, 10.0, 3.4)


def test_energy_consistency_check() -> None:
    assert energy_is_consistent(CHICKEN.per_100g)
    assert energy_is_consistent(OIL.per_100g)
    # kJ stored as kcal is the classic data-entry error
    assert not energy_is_consistent(Nutrients(502, 22.5, 2.6, 0, 0))
