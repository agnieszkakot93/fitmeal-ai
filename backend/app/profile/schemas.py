"""The stored health profile's schemas (PRD §7, §10 NutritionProfile).

The profile is the plan snapshot (:class:`app.plans.schemas.ProfileIn`) plus
optional body data, so ``POST /v1/plans`` can use either one. Unknown fields
are rejected, every number is bounded and validation errors hide the input.

The output schemas carry no bounds or cross-field rules: a profile saved under
older rules must still be readable and exportable after a rule is tightened.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Self

from pydantic import BaseModel, Field, model_validator

from app.nutrition.allergens import ExclusionCategory, Severity
from app.planner.inputs import PLAN_LENGTHS, MealType
from app.plans.schemas import ProfileIn, _Snapshot, to_profile

Sex = Literal["female", "male"]
ActivityLevel = Literal["sedentary", "light", "moderate", "active", "very_active"]


class BodyDataIn(_Snapshot):
    """Optional; used only to suggest targets. Every field may be left out."""

    # 18+ only (PRD §7); no date of birth is kept
    age: int | None = Field(default=None, ge=18, le=120)
    sex: Sex | None = None
    weight_kg: float | None = Field(default=None, ge=30, le=300)
    height_cm: float | None = Field(default=None, ge=120, le=250)
    activity_level: ActivityLevel | None = None


class HealthProfileIn(ProfileIn):
    body: BodyDataIn | None = None

    @model_validator(mode="after")
    def _valid(self) -> Self:
        # the meal rules (shares add up, names unique) don't depend on the plan length
        to_profile(self, days=PLAN_LENGTHS[0], prep_days=1)
        return self


class MealOut(BaseModel):
    name: str
    meal_type: MealType
    kcal_share: float


class ExclusionOut(BaseModel):
    category: ExclusionCategory
    severity: Severity
    term: str | None
    relaxed: bool


class BodyDataOut(BaseModel):
    age: int | None
    sex: Sex | None
    weight_kg: float | None
    height_cm: float | None
    activity_level: ActivityLevel | None


class HealthProfileOut(BaseModel):
    daily_kcal: float
    protein_min_g: float
    meals: list[MealOut]
    max_minutes: int | None
    equipment: list[str]
    exclusions: list[ExclusionOut]
    body: BodyDataOut | None
    version: int = Field(description="Bumped on every save")
    updated_at: datetime
