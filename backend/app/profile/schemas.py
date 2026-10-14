"""The stored health profile's schemas (PRD §7, §10 NutritionProfile).

The profile is the plan snapshot (:class:`app.plans.schemas.ProfileIn`) plus
optional body data, so ``POST /v1/plans`` can use either one. Unknown fields
are rejected, every number is bounded and validation errors hide the input.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Self

from pydantic import Field, model_validator

from app.planner.inputs import PLAN_LENGTHS
from app.plans.schemas import ProfileIn, _Snapshot, to_profile


class BodyDataIn(_Snapshot):
    """Optional; used only to suggest targets. Every field may be left out."""

    # 18+ only (PRD §7); no date of birth is kept
    age: int | None = Field(default=None, ge=18, le=120)
    sex: Literal["female", "male"] | None = None
    weight_kg: float | None = Field(default=None, ge=30, le=300)
    height_cm: float | None = Field(default=None, ge=120, le=250)
    activity_level: Literal["sedentary", "light", "moderate", "active", "very_active"] | None = None


class HealthProfileIn(ProfileIn):
    body: BodyDataIn | None = None

    @model_validator(mode="after")
    def _valid(self) -> Self:
        # the meal rules (shares add up, names unique) don't depend on the plan length
        to_profile(self, days=PLAN_LENGTHS[0], prep_days=1)
        return self


class HealthProfileOut(HealthProfileIn):
    version: int = Field(description="Bumped on every save")
    updated_at: datetime
