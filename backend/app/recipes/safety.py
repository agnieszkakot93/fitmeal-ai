"""Recipe-level allergens and exclusion checks (PRD §7, §8.1).

A recipe contains what any of its ingredients contains, may contain what any
of them may contain, and has unknown traces if any ingredient's traces are
unknown, since one unknown hides everything else. Optional ingredients count:
the recipe as written includes them.

A recipe with an ALLERGY or strict INTOLERANCE conflict in a required
ingredient is blocked from personalising and planning until that ingredient
is substituted. A conflicting optional ingredient is simply left out.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from app.nutrition.allergens import (
    Allergen,
    Exclusion,
    IngredientAllergens,
    TraceStatus,
    Verdict,
    classify_all,
)


@dataclass(frozen=True, slots=True)
class RecipeAllergens:
    contains: frozenset[Allergen]
    may_contain: frozenset[Allergen]
    trace_status: TraceStatus


def combine(ingredients: Iterable[IngredientAllergens]) -> RecipeAllergens:
    contains: set[Allergen] = set()
    may_contain: set[Allergen] = set()
    unknown = False
    for ingredient in ingredients:
        contains |= ingredient.contains
        may_contain |= ingredient.may_contain
        unknown = unknown or ingredient.trace_status is TraceStatus.UNKNOWN
    may_contain -= contains
    if unknown:
        status = TraceStatus.UNKNOWN
    elif may_contain:
        status = TraceStatus.DECLARED
    else:
        status = TraceStatus.NONE_DECLARED
    return RecipeAllergens(frozenset(contains), frozenset(may_contain), status)


@dataclass(frozen=True, slots=True)
class CheckLine:
    key: str
    allergens: IngredientAllergens
    optional: bool = False


@dataclass(frozen=True, slots=True)
class Conflict:
    key: str
    verdict: Verdict  # EXCLUDED or PENALISED
    optional: bool


@dataclass(frozen=True, slots=True)
class RecipeCheck:
    conflicts: list[Conflict]

    @property
    def blocked(self) -> bool:
        """A required ingredient is excluded: substitute it before planning."""
        return any(c.verdict is Verdict.EXCLUDED and not c.optional for c in self.conflicts)

    @property
    def must_remove(self) -> list[str]:
        """Excluded optional ingredients: leave them out."""
        return [c.key for c in self.conflicts if c.verdict is Verdict.EXCLUDED and c.optional]

    @property
    def must_substitute(self) -> list[str]:
        return [c.key for c in self.conflicts if c.verdict is Verdict.EXCLUDED and not c.optional]


def check(lines: Sequence[CheckLine], exclusions: Sequence[Exclusion]) -> RecipeCheck:
    conflicts = []
    for line in lines:
        verdict = classify_all(line.allergens, exclusions)
        if verdict is not Verdict.ALLOWED:
            conflicts.append(Conflict(line.key, verdict, line.optional))
    return RecipeCheck(conflicts)
