"""Substitution engine. Nutrition values are plausible test data, not reference data."""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from app.foods.vocab import CulinaryRole as R
from app.nutrition.allergens import (
    Allergen,
    Exclusion,
    ExclusionCategory,
    IngredientAllergens,
    Origin,
    Severity,
    TraceStatus,
)
from app.nutrition.nutrients import Nutrients, for_grams
from app.optimizer.substitute import MAX_RATIO, MIN_RATIO, Food, options


def food(
    key: str,
    n: Nutrients,
    roles: set[R],
    groups: set[str],
    origin: Origin = Origin.PLANT,
    contains: frozenset[Allergen] = frozenset(),
    water: float | None = None,
) -> Food:
    allergens = IngredientAllergens(
        origin=origin,
        contains=contains,
        names=(key,),
        trace_status=TraceStatus.NONE_DECLARED,
    )
    return Food(key, n, frozenset(roles), frozenset(groups), allergens, water)


CHICKEN = food("chicken", Nutrients(120, 22.5, 2.6, 0, 0), {R.MAIN_PROTEIN}, {"lean_poultry"},
               Origin.POULTRY, water=74)  # fmt: skip
TURKEY = food("turkey", Nutrients(114, 23.7, 1.5, 0, 0), {R.MAIN_PROTEIN}, {"lean_poultry"},
              Origin.POULTRY, water=74)  # fmt: skip
TOFU = food("tofu", Nutrients(144, 15.8, 8.7, 1.2, 2.3), {R.MAIN_PROTEIN}, {"plant_protein"},
            contains=frozenset({Allergen.SOY}), water=71)  # fmt: skip
SHRIMP = food("shrimp", Nutrients(85, 20, 0.5, 0, 0), {R.MAIN_PROTEIN}, {"seafood"},
              Origin.FISH, contains=frozenset({Allergen.CRUSTACEANS}), water=78)  # fmt: skip
RICE = food("rice", Nutrients(360, 6.6, 0.6, 79, 1.3), {R.CARB_BASE}, {"grain"})
OLIVE_OIL = food("olive-oil", Nutrients(884, 0, 100, 0, 0), {R.COOKING_FAT}, {"cooking_oil"})
BUTTER = food("butter", Nutrients(717, 0.9, 81, 0.1, 0), {R.COOKING_FAT}, {"cooking_fat"},
              Origin.DAIRY, contains=frozenset({Allergen.MILK}))  # fmt: skip

PROTEINS = [CHICKEN, TURKEY, TOFU, SHRIMP, RICE]


def test_same_group_ranks_first_and_role_mismatch_is_skipped() -> None:
    ranked = options(CHICKEN, 150, R.MAIN_PROTEIN, PROTEINS)
    assert ranked[0].key == "turkey"
    assert ranked[0].same_group
    assert "rice" not in {o.key for o in ranked}
    assert "chicken" not in {o.key for o in ranked}


def test_protein_swap_matches_protein_not_weight() -> None:
    tofu = next(o for o in options(CHICKEN, 150, R.MAIN_PROTEIN, PROTEINS) if o.key == "tofu")
    assert tofu.grams == pytest.approx(150 * 22.5 / 15.8)
    assert tofu.delta.protein_g == pytest.approx(0, abs=1e-6)
    assert tofu.delta.kcal > 0


def test_fat_swap_matches_fat() -> None:
    [butter] = options(OLIVE_OIL, 10, R.COOKING_FAT, [BUTTER])
    assert butter.grams == pytest.approx(10 * 100 / 81)


def test_allergy_is_never_offered_and_dislike_is_ranked_down() -> None:
    exclusions = [
        Exclusion(ExclusionCategory.CRUSTACEANS, Severity.ALLERGY),
        Exclusion(ExclusionCategory.OTHER, Severity.DISLIKE, term="turkey"),
    ]
    ranked = options(CHICKEN, 150, R.MAIN_PROTEIN, PROTEINS, exclusions)
    keys = [o.key for o in ranked]
    assert "shrimp" not in keys
    turkey = next(o for o in ranked if o.key == "turkey")
    assert turkey.disliked
    assert keys[0] == "tofu"


def test_strict_intolerance_excludes() -> None:
    exclusions = [Exclusion(ExclusionCategory.SOY, Severity.INTOLERANCE)]
    keys = {o.key for o in options(CHICKEN, 150, R.MAIN_PROTEIN, PROTEINS, exclusions)}
    assert "tofu" not in keys


def test_rejects_non_positive_grams() -> None:
    with pytest.raises(ValueError):
        options(CHICKEN, 0, R.MAIN_PROTEIN, PROTEINS)


@settings(max_examples=80, deadline=None)
@given(
    grams=st.floats(1, 1000),
    protein=st.floats(0, 40),
    fat=st.floats(0, 100),
    carbs=st.floats(0, 90),
    role=st.sampled_from([R.MAIN_PROTEIN, R.CARB_BASE, R.COOKING_FAT, R.VEGETABLE]),
)
def test_options_are_sound(grams: float, protein: float, fat: float, carbs: float, role: R) -> None:
    kcal = protein * 4 + fat * 9 + carbs * 4
    candidate = food("x", Nutrients(kcal, protein, fat, carbs, 0), {role}, {"g"})
    original = food("o", Nutrients(200, 20, 10, 10, 0), {role}, {"g"})
    [option] = options(original, grams, role, [candidate])
    assert MIN_RATIO * grams - 1e-9 <= option.grams <= MAX_RATIO * grams + 1e-9
    expected = for_grams(candidate.per_100g, option.grams) + for_grams(
        original.per_100g, grams
    ).scale(-1)
    assert option.delta.kcal == pytest.approx(expected.kcal)
    assert option.delta.protein_g == pytest.approx(expected.protein_g)
