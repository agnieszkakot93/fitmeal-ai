"""Allergens, derivation and the user-facing exclusion categories.

Allergens follow the 14 declarable allergens of EU Regulation 1169/2011.
A food's *effective* allergens are its own plus those of everything it is
derived from (whey → milk), computed transitively.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from enum import StrEnum


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


class ExclusionCategory(StrEnum):
    """The checklist the user sees in onboarding (PRD §7)."""

    FISH = "fish"
    SHELLFISH = "shellfish"
    MEAT = "meat"
    DAIRY = "dairy"
    EGGS = "eggs"
    GLUTEN = "gluten"
    SOY = "soy"
    NUTS = "nuts"


EXCLUSION_ALLERGENS: dict[ExclusionCategory, frozenset[Allergen]] = {
    ExclusionCategory.FISH: frozenset({Allergen.FISH}),
    ExclusionCategory.SHELLFISH: frozenset({Allergen.CRUSTACEANS, Allergen.MOLLUSCS}),
    ExclusionCategory.MEAT: frozenset(),
    ExclusionCategory.DAIRY: frozenset({Allergen.MILK}),
    ExclusionCategory.EGGS: frozenset({Allergen.EGGS}),
    ExclusionCategory.GLUTEN: frozenset({Allergen.GLUTEN}),
    ExclusionCategory.SOY: frozenset({Allergen.SOY}),
    ExclusionCategory.NUTS: frozenset({Allergen.TREE_NUTS, Allergen.PEANUTS}),
}

EXCLUSION_ORIGINS: dict[ExclusionCategory, frozenset[Origin]] = {
    ExclusionCategory.FISH: frozenset({Origin.FISH}),
    ExclusionCategory.SHELLFISH: frozenset({Origin.SHELLFISH}),
    ExclusionCategory.MEAT: frozenset({Origin.MEAT, Origin.POULTRY}),
    ExclusionCategory.DAIRY: frozenset({Origin.DAIRY}),
    ExclusionCategory.EGGS: frozenset({Origin.EGG}),
}


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
    result: dict[str, frozenset[Allergen]] = {}
    visiting: set[str] = set()

    def visit(key: str) -> frozenset[Allergen]:
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
    """Which of the user's excluded categories this food falls into."""
    food_allergens = set(allergens)
    hits: set[ExclusionCategory] = set()
    for category in excluded:
        if food_allergens & EXCLUSION_ALLERGENS[category]:
            hits.add(category)
        if origin in EXCLUSION_ORIGINS.get(category, frozenset()):
            hits.add(category)
    return hits
