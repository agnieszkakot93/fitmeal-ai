import pytest

from app.nutrition.units import FoodUnitData, UnitConversionError, resolve_unit, to_grams

OIL = FoodUnitData(density_g_per_ml=0.91)
FLOUR = FoodUnitData(density_g_per_ml=0.53, portions_g={"szklanka": 160})
GARLIC = FoodUnitData(portions_g={"clove": 4})


@pytest.mark.parametrize(
    ("raw", "code"),
    [
        ("g", "g"),
        ("Gramów", "g"),
        ("dkg", "dag"),
        ("łyżka", "tbsp"),
        ("Łyżki", "tbsp"),
        ("łyżeczki", "tsp"),
        ("szklanki", "szklanka"),
        ("cups", "cup"),
        ("szt.", "piece"),
        ("ząbki", "clove"),
        ("garść", "handful"),
        ("miarka", "scoop"),
    ],
)
def test_resolve_unit_handles_polish_forms_and_diacritics(raw: str, code: str) -> None:
    assert resolve_unit(raw).code == code


def test_unknown_unit_raises() -> None:
    with pytest.raises(UnitConversionError):
        resolve_unit("bucket")


def test_mass_units_need_no_food_data() -> None:
    assert to_grams(2, "kg", FoodUnitData()) == 2000
    assert to_grams(15, "dag", FoodUnitData()) == 150


def test_volume_uses_density() -> None:
    assert to_grams(1, "tbsp", OIL) == pytest.approx(15 * 0.91)
    assert to_grams(100, "ml", OIL) == pytest.approx(91)


def test_food_specific_volume_weight_beats_density() -> None:
    assert to_grams(1, "szklanka", FLOUR) == 160
    assert to_grams(1, "cup", FLOUR) == pytest.approx(240 * 0.53)


def test_portion_units_use_food_table() -> None:
    assert to_grams(3, "ząbki", GARLIC) == 12


def test_missing_density_or_portion_is_an_error_not_a_guess() -> None:
    with pytest.raises(UnitConversionError):
        to_grams(1, "cup", FoodUnitData())
    with pytest.raises(UnitConversionError):
        to_grams(1, "piece", GARLIC)


def test_negative_amount_rejected() -> None:
    with pytest.raises(ValueError):
        to_grams(-1, "g", FoodUnitData())
