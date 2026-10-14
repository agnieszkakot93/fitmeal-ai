"""A variant's ingredient lines and the swaps applied to them (PRD §8.4).

Pure functions: the caller loads the foods and ranks substitutes with the
Substitution Engine (:func:`app.optimizer.substitute.options`), which never
returns a food the user's ALLERGY or strict INTOLERANCE excludes.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, replace
from typing import Any

from app.foods.vocab import CulinaryRole
from app.nutrition.allergens import Exclusion, IngredientAllergens, Verdict
from app.nutrition.nutrients import Nutrients, for_grams
from app.optimizer.substitute import Option
from app.recipes.safety import CheckLine, check


@dataclass(frozen=True, slots=True)
class VariantLine:
    """One ingredient of one serving; ``key`` is the base recipe's ``<position>:<slug>``."""

    key: str
    position: int
    food: str  # slug of the food used now (the substitute if swapped)
    original_food: str
    original_g: float  # per serving in the base recipe
    grams: float  # per serving in the variant; 0 when removed
    role: CulinaryRole
    optional: bool
    removed: bool = False
    swapped: bool = False

    def to_json(self) -> dict[str, Any]:
        return asdict(self) | {"role": self.role.value}

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> VariantLine:
        return cls(**{**data, "role": CulinaryRole(data["role"])})


def nutrition(lines: Sequence[VariantLine], per_100g: Mapping[str, Nutrients]) -> Nutrients:
    """One serving's nutrition from the line weights."""
    return Nutrients.total(
        [for_grams(per_100g[line.food], line.grams) for line in lines if not line.removed]
    )


def choose(ranked: Sequence[Option], food: str | None) -> Option | None:
    """The user's pick among the ranked options; ``None`` picks the best one not disliked."""
    if food is None:
        liked = [o for o in ranked if not o.disliked] or list(ranked)
        return liked[0] if liked else None
    return next((o for o in ranked if o.key == food), None)


def substitute(lines: Sequence[VariantLine], key: str, option: Option) -> list[VariantLine]:
    return [
        replace(line, food=option.key, grams=round(option.grams, 1), swapped=True)
        if line.key == key
        else line
        for line in lines
    ]


def leave_out(lines: Sequence[VariantLine], key: str) -> list[VariantLine]:
    return [replace(line, grams=0.0, removed=True) if line.key == key else line for line in lines]


def conflicts(
    lines: Sequence[VariantLine],
    allergens: Mapping[str, IngredientAllergens],
    exclusions: Sequence[Exclusion],
) -> list[str]:
    """Keys of the lines still in the variant that the exclusions rule out."""
    checked = check(
        [
            CheckLine(line.key, allergens[line.food], line.optional)
            for line in lines
            if not line.removed
        ],
        exclusions,
    )
    return [c.key for c in checked.conflicts if c.verdict is Verdict.EXCLUDED]
