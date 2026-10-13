"""Request and response schemas for the plans API.

The profile snapshot in :class:`PlanIn` is used in memory to build the plan and
never stored or logged (D8 fallback, until the stored profile of D13 is wired
in). It rejects unknown fields, bounds every number and hides its input in
errors.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.foods.schemas import NutrientsOut
from app.planner.inputs import KCAL_FLOOR, MealSlot, MealType, Profile
from app.planner.result import Action, BlockerKind
from app.planner.solve import Rule, Status
from app.plans.models import SlotStatus
from app.recipes.schemas import MAX_EXCLUSIONS, Exclusions, to_exclusions


class _Snapshot(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True, allow_inf_nan=False)


class MealIn(_Snapshot):
    name: str = Field(min_length=1, max_length=40, pattern=r"^[a-z0-9_]+$")
    meal_type: MealType
    kcal_share: float = Field(gt=0, le=1, description="Share of the daily calories, 0-1")


class ProfileIn(_Snapshot):
    """The parts of the nutrition profile the planner needs (PRD §7)."""

    daily_kcal: float = Field(ge=KCAL_FLOOR, le=6000)
    protein_min_g: float = Field(ge=0, le=400)
    meals: list[MealIn] = Field(min_length=2, max_length=5)
    max_minutes: int | None = Field(default=None, ge=1, le=1440, description="None: no limit")
    equipment: list[str] = Field(default=[], max_length=20)
    exclusions: Exclusions = Field(default=[], max_length=MAX_EXCLUSIONS)


class PlanIn(_Snapshot):
    days: Literal[3, 5, 7]
    prep_days: int = Field(default=1, ge=1, le=3, description='"Cook once for N days"')
    profile: ProfileIn

    @model_validator(mode="after")
    def _valid(self) -> Self:
        self.to_profile()  # raises ValueError with the rule that was broken
        return self

    def to_profile(self) -> Profile:
        p = self.profile
        return Profile(
            daily_kcal=p.daily_kcal,
            protein_min_g=p.protein_min_g,
            meals=tuple(MealSlot(m.name, m.meal_type, m.kcal_share) for m in p.meals),
            days=self.days,
            prep_days=self.prep_days,
            max_minutes=p.max_minutes,
            equipment=frozenset(p.equipment),
            exclusions=tuple(to_exclusions(p.exclusions)),
        )


class SlotOut(BaseModel):
    position: int = Field(description="The slot's address in `/slots/{slot}`")
    day: int = Field(description="0-based")
    slot: str
    meal_type: MealType
    recipe_id: uuid.UUID | None = Field(description="None if the recipe was deleted since")
    recipe_slug: str | None
    title_en: str | None
    title_pl: str | None
    portion: float = Field(description="Servings of the recipe")
    nutrition: NutrientsOut
    cook_day: int
    eat_by_day: int
    from_batch: bool
    leave_out: list[str] = Field(description="Optional ingredient keys to leave out")
    labels: list[str] = Field(
        default=[],
        description="Soft exclusions the recipe touches. Only in the response that created "
        "the plan: they come from the profile, which is not stored.",
    )
    status: SlotStatus
    status_updated_at: datetime | None


class DayOut(BaseModel):
    day: int
    totals: NutrientsOut
    slots: list[SlotOut]


class TargetsOut(BaseModel):
    daily_kcal: float
    protein_min_g: float


class PlanOut(BaseModel):
    id: uuid.UUID
    created_at: datetime
    days: int
    prep_days: int
    targets: TargetsOut
    notices: list[str] = Field(description="Soft goals that had to be relaxed, in plain words")
    relaxed: list[Rule]
    plan_days: list[DayOut]


class BlockerOut(BaseModel):
    kind: BlockerKind
    message: str
    meal: str | None


class SuggestionOut(BaseModel):
    action: Action
    message: str
    value: str | int | None


class InfeasibleOut(BaseModel):
    """No plan fits the hard constraints: what blocked it and what to change (PRD §8.5)."""

    status: Status
    message: str
    blockers: list[BlockerOut]
    suggestions: list[SuggestionOut]


class InvalidBodyOut(BaseModel):
    """FastAPI's validation error, without the submitted values."""

    detail: list[dict[str, Any]]


class SlotStatusIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal[SlotStatus.COOKED, SlotStatus.EATEN, SlotStatus.SKIPPED]
    event_id: uuid.UUID = Field(
        description="Client-generated, unique per change: a replay with the same id is a no-op"
    )
