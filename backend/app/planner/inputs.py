"""What the planner is given: candidate recipes and a snapshot of the profile.

Everything here is a frozen value object; the planner never reads the database.
Nutrition is per serving, computed by the nutrition engine (PRD principle 2).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

from app.nutrition.allergens import Exclusion, Severity
from app.nutrition.nutrients import Nutrients
from app.recipes.safety import CheckLine

# No plan day may ever total below this, whatever the target (PRD §7, §8.5).
KCAL_FLOOR = 1200.0
# Each plan day within ±5% of the daily kcal target (PRD §8.5).
KCAL_TOLERANCE = 0.05
PLAN_LENGTHS = (3, 5, 7)


class MealType(StrEnum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


# Recipe tags that make a recipe fit a meal slot of each type.
MEAL_TYPE_TAGS: dict[MealType, frozenset[str]] = {
    MealType.BREAKFAST: frozenset({"breakfast"}),
    MealType.LUNCH: frozenset({"lunch"}),
    MealType.DINNER: frozenset({"dinner"}),
    MealType.SNACK: frozenset({"snack", "dessert"}),
}

# Tools every kitchen is assumed to have. The profile lists only appliances
# (oven, blender, air fryer...): onboarding asks about those, not about pots.
BASIC_TOOLS = frozenset(
    {"pot", "pan", "wok", "jar", "baking_tray", "muffin_tin", "loaf_tin", "ice_pop_moulds"}
)


@dataclass(frozen=True, slots=True)
class Candidate:
    """A recipe the planner may use.

    ``allergen_lines`` are the recipe's ingredients as the exclusion check sees
    them (:func:`app.recipes.safety.check`). A recipe with no lines is treated
    as unknown and never planned for a user with a hard exclusion.
    ``ingredient_ids`` (food ids or slugs), when given, drive ingredient reuse.
    """

    id: str
    tags: frozenset[str]
    per_serving: Nutrients
    servings: int
    fridge_days: int
    freezer_friendly: bool
    meal_prep_score: int  # 0-100 (PRD §8.7)
    total_minutes: int
    equipment: frozenset[str]
    allergen_lines: tuple[CheckLine, ...]
    ingredient_ids: frozenset[str] = frozenset()

    def fits(self, meal_type: MealType) -> bool:
        return bool(self.tags & MEAL_TYPE_TAGS[meal_type])


@dataclass(frozen=True, slots=True)
class MealSlot:
    """One meal of the day and its share of the daily calories (0-1)."""

    name: str
    meal_type: MealType
    kcal_share: float


@dataclass(frozen=True, slots=True)
class Profile:
    """The parts of the user's NutritionProfile the planner needs (PRD §7).

    ``max_minutes`` of ``None`` means no limit (the "60+" choice).
    ``prep_days`` is "cook once for N days": 1 means no batching.
    ``equipment`` lists the appliances the user has, beyond :data:`BASIC_TOOLS`.
    """

    daily_kcal: float
    protein_min_g: float
    meals: tuple[MealSlot, ...]
    days: int
    prep_days: int = 1
    max_minutes: int | None = None
    equipment: frozenset[str] = frozenset()
    exclusions: tuple[Exclusion, ...] = ()

    def __post_init__(self) -> None:
        if self.daily_kcal < KCAL_FLOOR:
            raise ValueError(f"daily target below the {KCAL_FLOOR:.0f} kcal floor")
        if self.protein_min_g < 0:
            raise ValueError("protein minimum must not be negative")
        if not 2 <= len(self.meals) <= 5:
            raise ValueError("a day has 2 to 5 meals")
        if len({m.name for m in self.meals}) != len(self.meals):
            raise ValueError("meal names must be unique")
        if any(m.kcal_share <= 0 for m in self.meals):
            raise ValueError("every meal needs a positive calorie share")
        if not math.isclose(sum(m.kcal_share for m in self.meals), 1.0, abs_tol=0.01):
            raise ValueError("meal calorie shares must add up to 100%")
        if self.days not in PLAN_LENGTHS:
            raise ValueError(f"plan length must be one of {PLAN_LENGTHS}")
        if not 1 <= self.prep_days <= 3:
            raise ValueError("cook once for 1 to 3 days")
        if self.max_minutes is not None and self.max_minutes <= 0:
            raise ValueError("max cooking time must be positive")

    @property
    def kcal_window(self) -> tuple[float, float]:
        """Allowed daily kcal: ±5% of the target, never below the floor (PRD §8.5)."""
        return max(KCAL_FLOOR, self.daily_kcal * (1 - KCAL_TOLERANCE)), self.daily_kcal * (
            1 + KCAL_TOLERANCE
        )

    @property
    def hard_exclusions(self) -> tuple[Exclusion, ...]:
        return tuple(
            e
            for e in self.exclusions
            if e.severity is Severity.ALLERGY
            or (e.severity is Severity.INTOLERANCE and not e.relaxed)
        )
