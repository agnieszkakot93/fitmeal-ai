"""Request and response schemas for variants, slot swaps and rebalancing.

Profile snapshots (exclusions, the plan profile) are used in memory and never
stored or logged (D8 fallback, when there is no stored D13 profile). They
reject unknown fields, bound every number and hide their input in errors.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.foods.schemas import NutrientsOut
from app.foods.vocab import CulinaryRole
from app.plans.schemas import ProfileIn, SlotOut
from app.recipes.schemas import (
    MAX_EXCLUSIONS,
    ExclusionIn,
    ExplanationOut,
    FoodRef,
    MealTarget,
    MissOut,
)


class _Snapshot(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True, allow_inf_nan=False)


_KEY = r"^\d{1,4}:[a-z0-9]+(-[a-z0-9]+)*$"
_SLUG = r"^[a-z0-9]+(-[a-z0-9]+)*$"


class SlotRefOut(BaseModel):
    plan_id: uuid.UUID
    slot: int = Field(description="The slot's position")


class VariantLineOut(BaseModel):
    key: str = Field(description="The base recipe's ingredient key, `<position>:<food slug>`")
    position: int
    food: FoodRef = Field(description="The food used now (the substitute if swapped)")
    original_food: str
    original_g: float = Field(description="Per serving in the base recipe")
    grams: float = Field(description="Per serving in the variant; 0 when removed")
    culinary_role: CulinaryRole
    optional: bool
    removed: bool
    swapped: bool


class VariantOut(BaseModel):
    """The user's saved version of a recipe, for one serving."""

    id: uuid.UUID
    recipe_id: uuid.UUID
    label: str | None
    target: MealTarget = Field(description="The meal target the variant was computed for")
    lines: list[VariantLineOut]
    original_nutrition: NutrientsOut = Field(description="One serving of the base recipe")
    nutrition: NutrientsOut = Field(description="One serving of the variant")
    on_target: bool
    misses: list[MissOut]
    explanations: list[ExplanationOut] = Field(
        description='"Why did Donut change this?": every change in plain words, oldest first'
    )
    plan_slots: list[SlotRefOut] = Field(description="Plan slots cooked from this variant")
    created_at: datetime


class SubstituteIn(_Snapshot):
    ingredient: str = Field(pattern=_KEY, max_length=120, description="The line's `key`")
    food: str | None = Field(
        default=None,
        pattern=_SLUG,
        max_length=120,
        description="The substitute's slug, from the substitutions endpoint. Leave it out for "
        '"I don\'t have this": Donut picks the best safe substitute, or leaves out an '
        "optional ingredient.",
    )
    exclusions: list[ExclusionIn] = Field(
        default=[],
        max_length=MAX_EXCLUSIONS,
        description="Used without a stored profile with health-data consent (D8 fallback); "
        "ignored when there is one.",
    )


class AdjustmentOut(BaseModel):
    slot: int = Field(description="The slot's position")
    slot_name: str
    portion_from: float
    portion_to: float
    delta: NutrientsOut


class RebalanceOut(BaseModel):
    """A proposal: nothing changes until it is applied (PRD §8.6)."""

    plan_id: uuid.UUID
    day: int
    needed: bool = Field(description="The day is outside its targets and some meals can move")
    within_tolerance: bool = Field(description="The day meets its targets with the adjustments")
    totals_before: NutrientsOut
    totals_after: NutrientsOut = Field(description="With every adjustment applied")
    kcal_off: float = Field(
        description="kcal above (positive) or below (negative) the day's window after the "
        "adjustments; 0 within it"
    )
    protein_short_g: float
    adjustments: list[AdjustmentOut]
    message: str


class SubstituteOut(BaseModel):
    variant: VariantOut
    change: ExplanationOut
    previous_nutrition: NutrientsOut
    nutrition: NutrientsOut
    delta: NutrientsOut = Field(description="New minus previous, one serving")
    conflicts: list[str] = Field(
        description="Keys of other lines the request's exclusions rule out: substitute them too"
    )
    rebalance: list[RebalanceOut] = Field(
        description="For each plan day using this variant that the change moved off target"
    )


class SwapOptionsIn(_Snapshot):
    profile: ProfileIn | None = Field(
        default=None,
        description="Snapshot used when there is no stored profile with health-data consent "
        "(D8 fallback). Ignored when there is one.",
    )
    limit: int = Field(default=10, ge=1, le=30)


class SwapOptionOut(BaseModel):
    recipe_id: uuid.UUID
    recipe_slug: str | None
    title_en: str | None
    title_pl: str | None
    portion: float = Field(description="Servings, sized like the meal it replaces")
    nutrition: NutrientsOut
    delta: NutrientsOut = Field(description="This option minus the current meal")
    day_totals: NutrientsOut = Field(description="The day with this option, before rebalancing")
    total_minutes: int
    leave_out: list[str] = Field(description="Optional ingredient keys to leave out")
    labels: list[str] = Field(description="Soft exclusions the recipe touches; never stored")
    score: int = Field(description="Higher fits better")


class SwapOptionsOut(BaseModel):
    slot: SlotOut
    options: list[SwapOptionOut]


class SwapIn(SwapOptionsIn):
    recipe_id: uuid.UUID
    portion: float | None = Field(
        default=None, ge=0.5, le=2.0, description="Servings; default: sized like the meal"
    )
    fixed: list[int] = Field(
        default=[],
        max_length=5,
        description="Positions of the day's meals the rebalance must not touch, e.g. ones "
        "earlier than now. Eaten and skipped meals are never touched.",
    )


class SwapOut(BaseModel):
    slot: SlotOut
    rebalance: RebalanceOut


class AdjustmentIn(_Snapshot):
    slot: int = Field(ge=0, le=1000, description="The slot's position")
    portion: float = Field(gt=0, le=2.5)


class RebalanceApplyIn(_Snapshot):
    """The adjustments the user accepted, from a rebalance proposal."""

    day: int = Field(ge=0, le=31)
    adjustments: list[AdjustmentIn] = Field(min_length=1, max_length=5)

    @model_validator(mode="after")
    def _unique(self) -> Self:
        if len({a.slot for a in self.adjustments}) != len(self.adjustments):
            raise ValueError("one adjustment per slot")
        return self
