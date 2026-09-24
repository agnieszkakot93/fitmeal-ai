"""Allergens, derivation and the user-facing exclusion categories.

Allergens follow the 14 declarable allergens of EU Regulation 1169/2011.
A food's *effective* allergens are its own plus those of everything it is
derived from (whey → milk), computed transitively. "May contain" (trace)
declarations are tracked separately from what a food contains, together with a
:class:`TraceStatus`: whether the traces are known at all. Unknown is its own
state and never means "none".

A user's :class:`Exclusion` pairs a category with a :class:`Severity`, and
:func:`classify` turns it into a :class:`Verdict` for one ingredient:

============================  =========  ===========  ==============
severity                      contains   may contain  traces unknown
============================  =========  ===========  ==============
allergy                       excluded   excluded     excluded
intolerance                   excluded   allowed      allowed
intolerance, relaxed by user  penalised  allowed      allowed
dislike / prefer not to eat   penalised  allowed      allowed
============================  =========  ===========  ==============

"Traces unknown" applies to categories backed by EU allergens: an allergy to
milk excludes every food whose traces are unknown, since any allergen could be
among them (the same rule as an unresolved ingredient, PRD §9). Categories with
no allergen behind them (``meat``, free-text ``other``) are unaffected.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum

from app.core.text import fold


class Allergen(StrEnum):
    GLUTEN = "gluten"
    CRUSTACEANS = "crustaceans"
    EGGS = "eggs"
    FISH = "fish"
    PEANUTS = "peanuts"
    SOY = "soy"
    MILK = "milk"
    TREE_NUTS = "tree_nuts"
    CELERY = "celery"
    MUSTARD = "mustard"
    SESAME = "sesame"
    SULPHITES = "sulphites"
    LUPIN = "lupin"
    MOLLUSCS = "molluscs"


class Origin(StrEnum):
    """What a food is, for diet rules that are not allergens (vegetarian etc.)."""

    MEAT = "meat"
    POULTRY = "poultry"
    FISH = "fish"
    SHELLFISH = "shellfish"
    DAIRY = "dairy"
    EGG = "egg"
    PLANT = "plant"
    FUNGI = "fungi"
    OTHER = "other"


class TraceStatus(StrEnum):
    """What is known about a food's "may contain" (trace) allergens."""

    UNKNOWN = "unknown"  # nobody has checked: any allergen could be a trace
    NONE_DECLARED = "none_declared"  # checked, and the source declares no traces
    DECLARED = "declared"  # checked, and ``may_contain`` lists them


class ExclusionCategory(StrEnum):
    """The checklist the user sees in onboarding (PRD §7).

    Every EU allergen is its own category, with the same value as its
    :class:`Allergen`. ``shellfish``, ``meat``, ``dairy`` and ``nuts`` are the
    broader groups the checklist also shows; ``other`` is a free-text term the
    user types in (see :class:`Exclusion`).
    """

    # EU Regulation 1169/2011, Annex II
    GLUTEN = "gluten"
    CRUSTACEANS = "crustaceans"
    EGGS = "eggs"
    FISH = "fish"
    PEANUTS = "peanuts"
    SOY = "soy"
    MILK = "milk"
    TREE_NUTS = "tree_nuts"
    CELERY = "celery"
    MUSTARD = "mustard"
    SESAME = "sesame"
    SULPHITES = "sulphites"
    LUPIN = "lupin"
    MOLLUSCS = "molluscs"
    # broader groups
    SHELLFISH = "shellfish"
    MEAT = "meat"
    DAIRY = "dairy"
    NUTS = "nuts"
    # free text, matched against ingredient names and tags
    OTHER = "other"


EXCLUSION_ALLERGENS: dict[ExclusionCategory, frozenset[Allergen]] = {
    **{ExclusionCategory(a.value): frozenset({a}) for a in Allergen},
    ExclusionCategory.SHELLFISH: frozenset({Allergen.CRUSTACEANS, Allergen.MOLLUSCS}),
    ExclusionCategory.MEAT: frozenset(),
    ExclusionCategory.DAIRY: frozenset({Allergen.MILK}),
    ExclusionCategory.NUTS: frozenset({Allergen.TREE_NUTS, Allergen.PEANUTS}),
    ExclusionCategory.OTHER: frozenset(),
}

# Origins back up the allergen tags: a dairy food missing its "milk" tag is
# still caught by a milk exclusion.
EXCLUSION_ORIGINS: dict[ExclusionCategory, frozenset[Origin]] = {
    ExclusionCategory.FISH: frozenset({Origin.FISH}),
    ExclusionCategory.SHELLFISH: frozenset({Origin.SHELLFISH}),
    ExclusionCategory.MEAT: frozenset({Origin.MEAT, Origin.POULTRY}),
    ExclusionCategory.MILK: frozenset({Origin.DAIRY}),
    ExclusionCategory.DAIRY: frozenset({Origin.DAIRY}),
    ExclusionCategory.EGGS: frozenset({Origin.EGG}),
}


class Severity(StrEnum):
    """How strongly the user wants to avoid a category (PRD §7)."""

    ALLERGY = "allergy"
    INTOLERANCE = "intolerance"
    DISLIKE = "dislike"
    PREFER_NOT = "prefer_not"


class Verdict(StrEnum):
    """What one exclusion means for one ingredient, from least to most strict."""

    ALLOWED = "allowed"
    PENALISED = "penalised"  # allowed, but scored down
    EXCLUDED = "excluded"  # hard constraint: never used


_STRICTNESS = {Verdict.ALLOWED: 0, Verdict.PENALISED: 1, Verdict.EXCLUDED: 2}


@dataclass(frozen=True, slots=True)
class Exclusion:
    """One entry of the user's exclusion list.

    ``term`` is the user-entered text for ``other`` and must be empty for every
    other category. ``relaxed`` lets the user downgrade an intolerance to
    "avoid when possible"; allergies can never be relaxed.
    """

    category: ExclusionCategory
    severity: Severity
    term: str | None = None
    relaxed: bool = False

    def __post_init__(self) -> None:
        if self.category is ExclusionCategory.OTHER:
            if self.term is None or not fold(self.term):
                raise ValueError("an 'other' exclusion needs a non-empty term")
        elif self.term is not None:
            raise ValueError(f"only 'other' exclusions take a term, not {self.category!r}")
        if self.relaxed and self.severity is not Severity.INTOLERANCE:
            raise ValueError("only an intolerance can be relaxed")


@dataclass(frozen=True, slots=True)
class IngredientAllergens:
    """What the exclusion check needs to know about one ingredient.

    ``contains``, ``may_contain`` and ``trace_status`` should be the
    *effective* values (see :func:`effective_allergens`,
    :func:`effective_traces` and :func:`effective_trace_status`). ``names`` are
    the names, aliases and tags a free-text exclusion is matched against.

    ``trace_status`` defaults to unknown, the safe side: a caller that forgets
    it gets a stricter check, never a looser one.
    """

    origin: Origin
    contains: frozenset[Allergen] = frozenset()
    may_contain: frozenset[Allergen] = frozenset()
    names: tuple[str, ...] = ()
    trace_status: TraceStatus = TraceStatus.UNKNOWN


class DerivationCycleError(ValueError):
    pass


def effective_allergens(
    direct: Mapping[str, Iterable[Allergen]],
    derived_from: Mapping[str, Iterable[str]],
) -> dict[str, frozenset[Allergen]]:
    """Transitive allergen closure over the derivation graph.

    ``direct`` maps food key → its own allergens; ``derived_from`` maps food
    key → keys of the foods it is made from. Unknown parents raise ``KeyError``
    so a typo in the data can never silently drop an allergen.
    """
    return _closure(direct, derived_from)


def _closure[T](
    direct: Mapping[str, Iterable[T]],
    derived_from: Mapping[str, Iterable[str]],
) -> dict[str, frozenset[T]]:
    result: dict[str, frozenset[T]] = {}
    visiting: set[str] = set()

    def visit(key: str) -> frozenset[T]:
        if key in result:
            return result[key]
        if key in visiting:
            raise DerivationCycleError(f"derivation cycle through {key!r}")
        if key not in direct:
            raise KeyError(f"unknown food in derivation graph: {key!r}")
        visiting.add(key)
        acc = set(direct[key])
        for parent in derived_from.get(key, ()):
            acc |= visit(parent)
        visiting.discard(key)
        result[key] = frozenset(acc)
        return result[key]

    for key in direct:
        visit(key)
    return result


def violates_exclusions(
    allergens: Iterable[Allergen],
    origin: Origin,
    excluded: Iterable[ExclusionCategory],
) -> set[ExclusionCategory]:
    """Which of the given categories this food *contains*.

    Ignores severity, traces and free-text ``other`` terms; use
    :func:`classify` to decide whether a food may be used.
    """
    food_allergens = set(allergens)
    hits: set[ExclusionCategory] = set()
    for category in excluded:
        if food_allergens & EXCLUSION_ALLERGENS[category]:
            hits.add(category)
        if origin in EXCLUSION_ORIGINS.get(category, frozenset()):
            hits.add(category)
    return hits


def effective_traces(
    direct: Mapping[str, Iterable[Allergen]],
    derived_from: Mapping[str, Iterable[str]],
    contains: Mapping[str, frozenset[Allergen]],
) -> dict[str, frozenset[Allergen]]:
    """Transitive "may contain" closure, minus what each food definitely contains.

    ``direct`` maps food key → its own trace declarations and must cover the
    same keys as the derivation graph; ``contains`` is the result of
    :func:`effective_allergens`.
    """
    closure = effective_allergens(direct, derived_from)
    return {key: traces - contains.get(key, frozenset()) for key, traces in closure.items()}


def effective_trace_status(
    direct: Mapping[str, TraceStatus],
    derived_from: Mapping[str, Iterable[str]],
    traces: Mapping[str, frozenset[Allergen]],
) -> dict[str, TraceStatus]:
    """Trace status after inheritance.

    Unknown anywhere in a food's derivation closure (itself or any ancestor)
    makes it unknown: a known child can never hide an unknown parent. Otherwise
    the status follows the effective traces (``traces``, the result of
    :func:`effective_traces`): declared if any remain, else none declared.
    """
    unknown_in = _closure(
        {key: [key] if status is TraceStatus.UNKNOWN else [] for key, status in direct.items()},
        derived_from,
    )
    result: dict[str, TraceStatus] = {}
    for key, unknown in unknown_in.items():
        if unknown:
            result[key] = TraceStatus.UNKNOWN
        elif traces.get(key):
            result[key] = TraceStatus.DECLARED
        else:
            result[key] = TraceStatus.NONE_DECLARED
    return result


def _matches_term(term: str, names: Iterable[str]) -> bool:
    # Substring, not whole-word: for a hard constraint, over-matching ("pea"
    # also hits "chickpeas") is the safe direction.
    needle = fold(term)
    return any(needle in fold(name) for name in names)


def _contains(ingredient: IngredientAllergens, exclusion: Exclusion) -> bool:
    if exclusion.category is ExclusionCategory.OTHER:
        assert exclusion.term is not None  # enforced by Exclusion.__post_init__
        return _matches_term(exclusion.term, ingredient.names)
    return bool(ingredient.contains & EXCLUSION_ALLERGENS[exclusion.category]) or (
        ingredient.origin in EXCLUSION_ORIGINS.get(exclusion.category, frozenset())
    )


def _traces(ingredient: IngredientAllergens, exclusion: Exclusion) -> bool:
    """Whether a trace of this category is declared or cannot be ruled out."""
    allergens = EXCLUSION_ALLERGENS[exclusion.category]
    if ingredient.trace_status is TraceStatus.UNKNOWN and allergens:
        return True
    return bool(ingredient.may_contain & allergens)


def classify(ingredient: IngredientAllergens, exclusion: Exclusion) -> Verdict:
    """What one of the user's exclusions means for this ingredient."""
    if _contains(ingredient, exclusion):
        if exclusion.severity is Severity.ALLERGY:
            return Verdict.EXCLUDED
        if exclusion.severity is Severity.INTOLERANCE and not exclusion.relaxed:
            return Verdict.EXCLUDED
        return Verdict.PENALISED
    if exclusion.severity is Severity.ALLERGY and _traces(ingredient, exclusion):
        return Verdict.EXCLUDED
    return Verdict.ALLOWED


def classify_all(ingredient: IngredientAllergens, exclusions: Iterable[Exclusion]) -> Verdict:
    """The strictest verdict across all of the user's exclusions."""
    return max(
        (classify(ingredient, e) for e in exclusions),
        key=_STRICTNESS.__getitem__,
        default=Verdict.ALLOWED,
    )
