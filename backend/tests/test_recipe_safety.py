from collections.abc import Set

from hypothesis import given
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
)
from app.recipes.safety import CheckLine, check, combine


def ing(
    contains: Set[Allergen] = frozenset(),
    may: Set[Allergen] = frozenset(),
    status: TraceStatus = TraceStatus.NONE_DECLARED,
    origin: Origin = Origin.PLANT,
    name: str = "x",
) -> IngredientAllergens:
    return IngredientAllergens(origin, frozenset(contains), frozenset(may), (name,), status)


def test_combine_unions_and_drops_traces_already_contained() -> None:
    result = combine(
        [
            ing({Allergen.EGGS}, {Allergen.MILK}, TraceStatus.DECLARED),
            ing({Allergen.MILK}),
            ing(may={Allergen.SESAME}, status=TraceStatus.DECLARED),
        ]
    )
    assert result.contains == {Allergen.EGGS, Allergen.MILK}
    assert result.may_contain == {Allergen.SESAME}
    assert result.trace_status is TraceStatus.DECLARED


def test_one_unknown_makes_the_recipe_unknown() -> None:
    assert combine([ing(), ing(status=TraceStatus.UNKNOWN)]).trace_status is TraceStatus.UNKNOWN
    assert combine([ing(), ing()]).trace_status is TraceStatus.NONE_DECLARED


def test_required_allergen_blocks_optional_one_is_removed() -> None:
    lines = [
        CheckLine("egg", ing({Allergen.EGGS}, origin=Origin.EGG)),
        CheckLine("cheese", ing({Allergen.MILK}, origin=Origin.DAIRY), optional=True),
        CheckLine("rice", ing()),
    ]
    egg_allergy = Exclusion(ExclusionCategory.EGGS, Severity.ALLERGY)
    milk_allergy = Exclusion(ExclusionCategory.DAIRY, Severity.ALLERGY)

    only_milk = check(lines, [milk_allergy])
    assert not only_milk.blocked
    assert only_milk.must_remove == ["cheese"]

    both = check(lines, [egg_allergy, milk_allergy])
    assert both.blocked
    assert both.must_substitute == ["egg"]


def test_allergy_treats_unknown_traces_as_a_conflict_dislike_only_penalises() -> None:
    lines = [
        CheckLine("oil", ing(status=TraceStatus.UNKNOWN)),
        CheckLine("onion", ing(name="onion")),
    ]
    result = check(
        lines,
        [
            Exclusion(ExclusionCategory.PEANUTS, Severity.ALLERGY),
            Exclusion(ExclusionCategory.OTHER, Severity.DISLIKE, term="onion"),
        ],
    )
    verdicts = {c.key: c.verdict for c in result.conflicts}
    assert verdicts == {"oil": Verdict.EXCLUDED, "onion": Verdict.PENALISED}
    assert result.blocked


_allergens = st.frozensets(st.sampled_from(list(Allergen)))
_ingredients = st.builds(
    ing,
    contains=_allergens,
    may=_allergens,
    status=st.sampled_from(list(TraceStatus)),
)


@given(st.lists(_ingredients, min_size=1, max_size=6), _ingredients)
def test_adding_an_ingredient_never_makes_a_recipe_safer(
    base: list[IngredientAllergens], extra: IngredientAllergens
) -> None:
    before = combine(base)
    after = combine([*base, extra])
    assert before.contains <= after.contains
    assert before.contains | before.may_contain <= after.contains | after.may_contain
    assert not after.contains & after.may_contain
    if before.trace_status is TraceStatus.UNKNOWN:
        assert after.trace_status is TraceStatus.UNKNOWN
