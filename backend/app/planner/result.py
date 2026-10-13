"""What the planner returns: a plan, or a report of why there is none."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.nutrition.nutrients import Nutrients
from app.planner.solve import Rule, Status


@dataclass(frozen=True, slots=True)
class PlannedMeal:
    day: int  # 0-based
    slot: str
    recipe_id: str
    portion: float  # servings of the recipe
    nutrition: Nutrients
    cook_day: int  # == day unless eaten from a batch cooked earlier
    eat_by_day: int
    from_batch: bool
    leave_out: tuple[str, ...]  # excluded optional ingredients
    labels: tuple[str, ...]  # soft exclusions the recipe touches, shown on it


@dataclass(frozen=True, slots=True)
class DayPlan:
    day: int
    meals: tuple[PlannedMeal, ...]

    @property
    def totals(self) -> Nutrients:
        return Nutrients.total([m.nutrition for m in self.meals])


@dataclass(frozen=True, slots=True)
class Plan:
    days: tuple[DayPlan, ...]
    notices: tuple[str, ...]  # soft goals that had to be relaxed, in plain words
    relaxed: frozenset[Rule] = frozenset()

    @property
    def meals(self) -> tuple[PlannedMeal, ...]:
        return tuple(m for d in self.days for m in d.meals)


class BlockerKind(StrEnum):
    NO_RECIPES = "no_recipes"  # no recipe of this meal type at all
    FILTERED = "filtered"  # recipes exist, but none pass the hard filters
    PROTEIN = "protein"
    KCAL = "kcal"
    KCAL_AND_PROTEIN = "kcal_and_protein"
    TIMEOUT = "timeout"


@dataclass(frozen=True, slots=True)
class Blocker:
    kind: BlockerKind
    message: str
    meal: str | None = None  # the slot it is about, if any


class Action(StrEnum):
    MAX_MINUTES = "max_minutes"  # value: the new limit in minutes, None for no limit
    ADD_EQUIPMENT = "add_equipment"  # value: the appliance
    RELAX_INTOLERANCE = "relax_intolerance"  # value: the exclusion category
    SHORTEN_PLAN = "shorten_plan"  # value: the plan length in days
    LOWER_PROTEIN = "lower_protein"
    CHANGE_KCAL = "change_kcal"
    ADD_RECIPES = "add_recipes"  # value: the meal type
    RETRY = "retry"


@dataclass(frozen=True, slots=True)
class Suggestion:
    action: Action
    message: str
    value: str | int | None = None


@dataclass(frozen=True, slots=True)
class Infeasible:
    """No plan: what blocked it and what the user can change (PRD §8.5)."""

    status: Status
    blockers: tuple[Blocker, ...]
    suggestions: tuple[Suggestion, ...]

    @property
    def message(self) -> str:
        lines = [b.message for b in self.blockers]
        if self.suggestions:
            lines.append("You could:")
            lines += [f"- {s.message}" for s in self.suggestions]
        return "\n".join(lines)
