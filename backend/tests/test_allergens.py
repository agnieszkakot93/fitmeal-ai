import pytest

from app.nutrition.allergens import (
    Allergen,
    DerivationCycleError,
    ExclusionCategory,
    Origin,
    effective_allergens,
    violates_exclusions,
)


def test_allergens_inherit_transitively() -> None:
    result = effective_allergens(
        direct={"milk": [Allergen.MILK], "whey": [], "protein-bar": [Allergen.PEANUTS]},
        derived_from={"whey": ["milk"], "protein-bar": ["whey"]},
    )
    assert result["whey"] == {Allergen.MILK}
    assert result["protein-bar"] == {Allergen.MILK, Allergen.PEANUTS}


def test_unknown_parent_fails_loudly() -> None:
    with pytest.raises(KeyError):
        effective_allergens({"whey": []}, {"whey": ["milk"]})


def test_cycle_detected() -> None:
    with pytest.raises(DerivationCycleError):
        effective_allergens({"a": [], "b": []}, {"a": ["b"], "b": ["a"]})


def test_exclusions_match_by_allergen_and_origin() -> None:
    assert violates_exclusions([Allergen.FISH], Origin.FISH, [ExclusionCategory.FISH]) == {
        ExclusionCategory.FISH
    }
    # meat is an origin, not an allergen
    assert violates_exclusions([], Origin.POULTRY, [ExclusionCategory.MEAT]) == {
        ExclusionCategory.MEAT
    }
    # whey: origin dairy and inherited milk allergen both hit "dairy"
    assert violates_exclusions([Allergen.MILK], Origin.OTHER, [ExclusionCategory.DAIRY]) == {
        ExclusionCategory.DAIRY
    }
    assert violates_exclusions([Allergen.PEANUTS], Origin.PLANT, [ExclusionCategory.NUTS]) == {
        ExclusionCategory.NUTS
    }
    assert violates_exclusions([], Origin.PLANT, list(ExclusionCategory)) == set()
