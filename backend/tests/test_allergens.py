import itertools
import random
from collections.abc import Callable

import pytest

from app.nutrition.allergens import (
    EXCLUSION_ALLERGENS,
    Allergen,
    DerivationCycleError,
    Exclusion,
    ExclusionCategory,
    IngredientAllergens,
    Origin,
    Severity,
    Verdict,
    classify,
    classify_all,
    effective_allergens,
    effective_traces,
    violates_exclusions,
)

Cat = ExclusionCategory

ALLERGEN_CATEGORIES = [c for c in ExclusionCategory if EXCLUSION_ALLERGENS[c]]


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


def test_traces_inherit_and_drop_what_is_contained() -> None:
    direct = {"chocolate": [Allergen.PEANUTS, Allergen.MILK], "bar": [Allergen.SESAME]}
    derived_from = {"bar": ["chocolate"]}
    contains = {"chocolate": frozenset({Allergen.MILK}), "bar": frozenset({Allergen.MILK})}
    result = effective_traces(direct, derived_from, contains)
    assert result["chocolate"] == {Allergen.PEANUTS}
    assert result["bar"] == {Allergen.PEANUTS, Allergen.SESAME}


def test_exclusions_match_by_allergen_and_origin() -> None:
    assert violates_exclusions([Allergen.FISH], Origin.FISH, [Cat.FISH]) == {Cat.FISH}
    # meat is an origin, not an allergen
    assert violates_exclusions([], Origin.POULTRY, [Cat.MEAT]) == {Cat.MEAT}
    # whey: origin dairy and inherited milk allergen both hit "dairy"
    assert violates_exclusions([Allergen.MILK], Origin.OTHER, [Cat.DAIRY]) == {Cat.DAIRY}
    assert violates_exclusions([Allergen.PEANUTS], Origin.PLANT, [Cat.NUTS]) == {Cat.NUTS}
    assert violates_exclusions([], Origin.PLANT, list(ExclusionCategory)) == set()


def test_every_eu_allergen_is_its_own_category() -> None:
    for allergen in Allergen:
        assert EXCLUSION_ALLERGENS[ExclusionCategory(allergen.value)] == {allergen}
    assert set(EXCLUSION_ALLERGENS) == set(ExclusionCategory)


def test_onboarding_checklist_values_are_kept() -> None:
    legacy = {"fish", "shellfish", "meat", "dairy", "eggs", "gluten", "soy", "nuts", "other"}
    assert legacy <= {c.value for c in ExclusionCategory}


def ingredient(
    contains: frozenset[Allergen] = frozenset(),
    may_contain: frozenset[Allergen] = frozenset(),
    origin: Origin = Origin.PLANT,
    names: tuple[str, ...] = (),
) -> IngredientAllergens:
    return IngredientAllergens(origin, contains, may_contain, names)


PEANUT = frozenset({Allergen.PEANUTS})


@pytest.mark.parametrize(
    ("severity", "relaxed", "contains", "traces"),
    [
        (Severity.ALLERGY, False, Verdict.EXCLUDED, Verdict.EXCLUDED),
        (Severity.INTOLERANCE, False, Verdict.EXCLUDED, Verdict.ALLOWED),
        (Severity.INTOLERANCE, True, Verdict.PENALISED, Verdict.ALLOWED),
        (Severity.DISLIKE, False, Verdict.PENALISED, Verdict.ALLOWED),
        (Severity.PREFER_NOT, False, Verdict.PENALISED, Verdict.ALLOWED),
    ],
)
def test_severity_semantics(
    severity: Severity, relaxed: bool, contains: Verdict, traces: Verdict
) -> None:
    exclusion = Exclusion(Cat.PEANUTS, severity, relaxed=relaxed)
    assert classify(ingredient(contains=PEANUT), exclusion) is contains
    assert classify(ingredient(may_contain=PEANUT), exclusion) is traces
    assert classify(ingredient(), exclusion) is Verdict.ALLOWED


def test_default_is_no_traces() -> None:
    food = IngredientAllergens(Origin.PLANT, contains=PEANUT)
    assert food.may_contain == frozenset()


def test_origin_backs_up_missing_allergen_tag() -> None:
    untagged_cheese = ingredient(origin=Origin.DAIRY)
    assert classify(untagged_cheese, Exclusion(Cat.MILK, Severity.ALLERGY)) is Verdict.EXCLUDED


def test_group_categories_cover_their_allergens() -> None:
    mussels = ingredient(contains=frozenset({Allergen.MOLLUSCS}), origin=Origin.SHELLFISH)
    assert classify(mussels, Exclusion(Cat.SHELLFISH, Severity.ALLERGY)) is Verdict.EXCLUDED
    assert classify(mussels, Exclusion(Cat.MOLLUSCS, Severity.ALLERGY)) is Verdict.EXCLUDED
    assert classify(mussels, Exclusion(Cat.CRUSTACEANS, Severity.ALLERGY)) is Verdict.ALLOWED
    traced = ingredient(may_contain=frozenset({Allergen.TREE_NUTS}))
    assert classify(traced, Exclusion(Cat.NUTS, Severity.ALLERGY)) is Verdict.EXCLUDED


@pytest.mark.parametrize("term", ["Coriander", "  coriander ", "KOLENDRA", "kolendrą"])
def test_other_term_matches_names_case_and_accent_insensitively(term: str) -> None:
    food = ingredient(names=("Fresh coriander", "kolendrą"))
    assert classify(food, Exclusion(Cat.OTHER, Severity.ALLERGY, term=term)) is Verdict.EXCLUDED
    assert classify(food, Exclusion(Cat.OTHER, Severity.DISLIKE, term=term)) is Verdict.PENALISED


def test_other_term_matches_tags_and_ignores_unrelated_foods() -> None:
    food = ingredient(names=("Pesto", "herb_sauce"))
    assert classify(food, Exclusion(Cat.OTHER, Severity.ALLERGY, "herb")) is Verdict.EXCLUDED
    assert classify(food, Exclusion(Cat.OTHER, Severity.ALLERGY, "garlic")) is Verdict.ALLOWED


@pytest.mark.parametrize(
    "build",
    [
        lambda: Exclusion(Cat.OTHER, Severity.ALLERGY),
        lambda: Exclusion(Cat.OTHER, Severity.ALLERGY, term="   "),
        lambda: Exclusion(Cat.FISH, Severity.ALLERGY, term="salmon"),
        lambda: Exclusion(Cat.FISH, Severity.ALLERGY, relaxed=True),
        lambda: Exclusion(Cat.FISH, Severity.DISLIKE, relaxed=True),
    ],
)
def test_invalid_exclusions_rejected(build: Callable[[], Exclusion]) -> None:
    with pytest.raises(ValueError):
        build()


def test_classify_all_takes_the_strictest() -> None:
    food = ingredient(contains=frozenset({Allergen.MILK}), may_contain=PEANUT)
    dislike_milk = Exclusion(Cat.MILK, Severity.DISLIKE)
    peanut_intolerance = Exclusion(Cat.PEANUTS, Severity.INTOLERANCE)
    peanut_allergy = Exclusion(Cat.PEANUTS, Severity.ALLERGY)
    assert classify_all(food, []) is Verdict.ALLOWED
    assert classify_all(food, [peanut_intolerance]) is Verdict.ALLOWED
    assert classify_all(food, [dislike_milk, peanut_intolerance]) is Verdict.PENALISED
    assert classify_all(food, [dislike_milk, peanut_allergy]) is Verdict.EXCLUDED


# ── Properties ──────────────────────────────────────────────────────────────
# hypothesis is not a dependency yet, so these enumerate the (finite) space of
# category x allergen x origin exhaustively, and sample random combinations
# with fixed seeds.


@pytest.mark.parametrize("category", ALLERGEN_CATEGORIES)
def test_allergy_excludes_every_contained_or_traced_allergen(category: ExclusionCategory) -> None:
    allergy = Exclusion(category, Severity.ALLERGY)
    for allergen, origin, as_trace in itertools.product(
        EXCLUSION_ALLERGENS[category], Origin, [False, True]
    ):
        hit = frozenset({allergen})
        food = ingredient(
            contains=frozenset() if as_trace else hit,
            may_contain=hit if as_trace else frozenset(),
            origin=origin,
        )
        assert classify(food, allergy) is Verdict.EXCLUDED, (category, allergen, origin)


def random_ingredient(rng: random.Random) -> IngredientAllergens:
    allergens = list(Allergen)
    return ingredient(
        contains=frozenset(rng.sample(allergens, rng.randint(0, 3))),
        may_contain=frozenset(rng.sample(allergens, rng.randint(0, 3))),
        origin=rng.choice(list(Origin)),
    )


def random_exclusions(rng: random.Random) -> list[Exclusion]:
    exclusions = []
    for category in rng.sample(ALLERGEN_CATEGORIES, rng.randint(1, 5)):
        severity = rng.choice(list(Severity))
        relaxed = severity is Severity.INTOLERANCE and rng.random() < 0.5
        exclusions.append(Exclusion(category, severity, relaxed=relaxed))
    return exclusions


@pytest.mark.parametrize("seed", range(20))
def test_no_allergy_hit_is_ever_allowed(seed: int) -> None:
    rng = random.Random(seed)
    for _ in range(500):
        food = random_ingredient(rng)
        exclusions = random_exclusions(rng)
        present = food.contains | food.may_contain
        allergic_hit = any(
            e.severity is Severity.ALLERGY and present & EXCLUSION_ALLERGENS[e.category]
            for e in exclusions
        )
        if allergic_hit:
            assert classify_all(food, exclusions) is Verdict.EXCLUDED, (food, exclusions)


@pytest.mark.parametrize("seed", range(20))
def test_only_hard_contains_or_allergy_traces_exclude(seed: int) -> None:
    rng = random.Random(seed)
    for _ in range(500):
        food = random_ingredient(rng)
        for exclusion in random_exclusions(rng):
            verdict = classify(food, exclusion)
            if exclusion.severity is Severity.ALLERGY:
                continue
            traces_only = ingredient(may_contain=food.contains | food.may_contain)
            assert classify(traces_only, exclusion) is Verdict.ALLOWED
            if verdict is Verdict.EXCLUDED:
                assert exclusion.severity is Severity.INTOLERANCE
                assert not exclusion.relaxed


@pytest.mark.parametrize("seed", range(20))
def test_more_exclusions_are_never_less_strict(seed: int) -> None:
    rng = random.Random(seed)
    strictness = list(Verdict)
    for _ in range(500):
        food = random_ingredient(rng)
        base = random_exclusions(rng)
        extra = random_exclusions(rng)
        before = strictness.index(classify_all(food, base))
        after = strictness.index(classify_all(food, base + extra))
        assert after >= before
