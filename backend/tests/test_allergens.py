import itertools
from collections.abc import Callable
from dataclasses import replace

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

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
# The first test enumerates category x allergen x origin exhaustively; the rest
# are hypothesis properties over generated ingredients and exclusion lists.


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


ingredients = st.builds(
    IngredientAllergens,
    origin=st.sampled_from(Origin),
    contains=st.frozensets(st.sampled_from(Allergen), max_size=4),
    may_contain=st.frozensets(st.sampled_from(Allergen), max_size=4),
    names=st.lists(st.text(max_size=20), max_size=3).map(tuple),
)

WORD = st.text(alphabet="abcdefghijklmnopqrstuvwxyząćęłńóśźż", min_size=1, max_size=8)


@st.composite
def exclusions(draw: st.DrawFn) -> Exclusion:
    category = draw(st.sampled_from(ExclusionCategory))
    severity = draw(st.sampled_from(Severity))
    relaxed = severity is Severity.INTOLERANCE and draw(st.booleans())
    term = draw(WORD) if category is ExclusionCategory.OTHER else None
    return Exclusion(category, severity, term=term, relaxed=relaxed)


exclusion_lists = st.lists(exclusions(), max_size=6)


def strictness(verdict: Verdict) -> int:
    return list(Verdict).index(verdict)


@settings(max_examples=500)
@given(
    food=ingredients,
    category=st.sampled_from(ALLERGEN_CATEGORIES),
    as_trace=st.booleans(),
    others=exclusion_lists,
    data=st.data(),
)
def test_no_allergy_hit_is_ever_allowed(
    food: IngredientAllergens,
    category: ExclusionCategory,
    as_trace: bool,
    others: list[Exclusion],
    data: st.DataObject,
) -> None:
    allergen = data.draw(st.sampled_from(sorted(EXCLUSION_ALLERGENS[category])))
    if as_trace:
        food = replace(food, may_contain=food.may_contain | {allergen})
    else:
        food = replace(food, contains=food.contains | {allergen})
    user = data.draw(st.permutations([*others, Exclusion(category, Severity.ALLERGY)]))
    assert classify_all(food, user) is Verdict.EXCLUDED


@settings(max_examples=500)
@given(
    food=ingredients,
    term=WORD,
    prefix=st.text(max_size=5),
    suffix=st.text(max_size=5),
    others=exclusion_lists,
)
def test_no_allergy_to_a_free_text_term_is_ever_allowed(
    food: IngredientAllergens, term: str, prefix: str, suffix: str, others: list[Exclusion]
) -> None:
    food = replace(food, names=(*food.names, f"{prefix} {term.upper()} {suffix}"))
    allergy = Exclusion(ExclusionCategory.OTHER, Severity.ALLERGY, term=term)
    assert classify_all(food, [*others, allergy]) is Verdict.EXCLUDED


@given(food=ingredients, exclusion=exclusions())
def test_only_allergies_exclude_on_traces(food: IngredientAllergens, exclusion: Exclusion) -> None:
    traces_only = ingredient(may_contain=food.contains | food.may_contain)
    if exclusion.severity is not Severity.ALLERGY:
        assert classify(traces_only, exclusion) is Verdict.ALLOWED
    if classify(food, exclusion) is Verdict.EXCLUDED:
        assert exclusion.severity is Severity.ALLERGY or (
            exclusion.severity is Severity.INTOLERANCE and not exclusion.relaxed
        )


@given(food=ingredients, base=exclusion_lists, extra=exclusion_lists)
def test_more_exclusions_are_never_less_strict(
    food: IngredientAllergens, base: list[Exclusion], extra: list[Exclusion]
) -> None:
    before = strictness(classify_all(food, base))
    assert strictness(classify_all(food, [*base, *extra])) >= before


@given(food=ingredients, user=exclusion_lists)
def test_confirming_a_trace_is_never_less_strict(
    food: IngredientAllergens, user: list[Exclusion]
) -> None:
    confirmed = replace(food, contains=food.contains | food.may_contain, may_contain=frozenset())
    assert strictness(classify_all(confirmed, user)) >= strictness(classify_all(food, user))
