"""Substitution Engine v1 (PRD §8.4).

Ranks replacements for one ingredient line. Never a naive 1:1 swap: the
amount is scaled so the substitute does the same job (same protein for a
main protein, same carbs for a carb base, same fat for a cooking fat), within
sensible limits. Candidates come from the same substitution group (close
swaps, e.g. chicken → turkey) or the same culinary role (wider swaps, e.g.
chicken → tofu). Anything the user's ALLERGY or strict INTOLERANCE excludes
is never returned; dislikes are ranked down, not hidden.

Pure functions only. Price deltas wait for estimated pricing (Phase 2).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from app.foods.vocab import CulinaryRole
from app.nutrition.allergens import Exclusion, IngredientAllergens, Verdict, classify_all
from app.nutrition.nutrients import Nutrients, for_grams

# substitute grams / original grams stays within these
MIN_RATIO = 0.5
MAX_RATIO = 2.0

# the nutrient a substitute must match for each role; other roles keep the weight
MATCH_NUTRIENT: dict[CulinaryRole, str] = {
    CulinaryRole.MAIN_PROTEIN: "protein_g",
    CulinaryRole.CARB_BASE: "carbs_g",
    CulinaryRole.COOKING_FAT: "fat_g",
}

# ranking penalties (lower score ranks first)
_P_OTHER_GROUP = 0.5  # same role, different substitution group
_P_DISLIKED = 3.0  # PRD §7: a strong penalty, below any acceptable swap
_P_WATER = 0.5  # per 100 g/100 g difference in water: cooks differently


@dataclass(frozen=True, slots=True)
class Food:
    key: str
    per_100g: Nutrients
    roles: frozenset[CulinaryRole]
    groups: frozenset[str]
    allergens: IngredientAllergens
    water_g: float | None = None


@dataclass(frozen=True, slots=True)
class Option:
    key: str
    grams: float
    same_group: bool
    disliked: bool
    delta: Nutrients  # substitute minus original, for the whole line
    score: float


def substitute_grams(original: Food, grams: float, candidate: Food, role: CulinaryRole) -> float:
    attr = MATCH_NUTRIENT.get(role)
    ratio = 1.0
    if attr is not None:
        have = getattr(original.per_100g, attr)
        per_g = getattr(candidate.per_100g, attr)
        if have > 0 and per_g > 0:
            ratio = have / per_g
    return grams * min(max(ratio, MIN_RATIO), MAX_RATIO)


def options(
    original: Food,
    grams: float,
    role: CulinaryRole,
    candidates: list[Food],
    exclusions: Sequence[Exclusion] = (),
    limit: int = 5,
) -> list[Option]:
    """Ranked substitutes for ``grams`` of ``original`` used as ``role``."""
    if grams <= 0:
        raise ValueError("grams must be positive")
    before = for_grams(original.per_100g, grams)
    ranked = []
    for food in candidates:
        if food.key == original.key or role not in food.roles:
            continue
        verdict = classify_all(food.allergens, exclusions)
        if verdict is Verdict.EXCLUDED:
            continue
        same_group = bool(food.groups & original.groups)
        amount = substitute_grams(original, grams, food, role)
        delta = for_grams(food.per_100g, amount) + before.scale(-1)
        ranked.append(
            Option(
                key=food.key,
                grams=amount,
                same_group=same_group,
                disliked=verdict is Verdict.PENALISED,
                delta=delta,
                score=_score(original, food, before, delta, same_group, verdict),
            )
        )
    ranked.sort(key=lambda o: (o.score, o.key))
    return ranked[:limit]


def _score(
    original: Food,
    food: Food,
    before: Nutrients,
    delta: Nutrients,
    same_group: bool,
    verdict: Verdict,
) -> float:
    score = abs(delta.kcal) / max(before.kcal, 50.0)
    score += abs(delta.protein_g) / max(before.protein_g, 5.0)
    if not same_group:
        score += _P_OTHER_GROUP
    if verdict is Verdict.PENALISED:
        score += _P_DISLIKED
    if original.water_g is not None and food.water_g is not None:
        score += _P_WATER * abs(original.water_g - food.water_g) / 100
    return score
