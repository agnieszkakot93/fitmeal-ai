"""Step 2: rank each allowed candidate for each meal slot (PRD §8.5).

The score adds macro fit, portion fit and meal-prep fit, minus penalties for
soft exclusions. It is in integer points so the CP-SAT objective can use it
directly. Ingredient reuse depends on the whole plan and is scored by the
solver (:mod:`app.planner.solve`).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from app.nutrition.allergens import Severity
from app.planner.filter import Screened
from app.planner.inputs import MealSlot, Profile

MACRO_WEIGHT = 300
PORTION_WEIGHT = 100
MEAL_PREP_WEIGHT = 200
# Per soft exclusion the recipe touches. A relaxed intolerance is used "only
# when no reasonable alternative exists" (PRD §7), so it costs the most.
SEVERITY_PENALTY: dict[Severity, int] = {
    Severity.INTOLERANCE: 600,  # relaxed by the user
    Severity.DISLIKE: 400,
    Severity.PREFER_NOT: 150,
}


@dataclass(frozen=True, slots=True)
class Score:
    macro: int
    portion: int
    meal_prep: int
    penalty: int

    @property
    def total(self) -> int:
        return self.macro + self.portion + self.meal_prep - self.penalty


def score(screened: Screened, slot: MealSlot, profile: Profile) -> Score:
    n = screened.candidate.per_serving
    # Protein per kcal against what the day needs: a recipe at or above the
    # daily ratio can't pull the day below the minimum.
    needed = profile.protein_min_g / profile.daily_kcal
    density = n.protein_g / n.kcal if n.kcal > 0 else 0.0
    macro = 1.0 if needed == 0 else min(1.0, density / needed)
    # How far one serving is from the slot's calories; 0.5x or 2x scores zero.
    target = profile.daily_kcal * slot.kcal_share
    portion = max(0.0, 1 - abs(math.log2(target / n.kcal))) if n.kcal > 0 else 0.0
    prep = screened.candidate.meal_prep_score / 100 if profile.prep_days > 1 else 0.0
    penalty = sum(SEVERITY_PENALTY[p.exclusion.severity] for p in screened.penalties)
    return Score(
        macro=round(MACRO_WEIGHT * macro),
        portion=round(PORTION_WEIGHT * portion),
        meal_prep=round(MEAL_PREP_WEIGHT * prep),
        penalty=penalty,
    )
