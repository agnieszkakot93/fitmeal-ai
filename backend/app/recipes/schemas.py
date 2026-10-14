"""Request and response schemas for the recipes API.

The profile snapshot (meal target, exclusions with tiers) arrives with each
request and is never stored or logged (Development Plan D8). Its schemas
reject unknown fields, bound every number and hide their input in errors.
"""

from __future__ import annotations

import uuid
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.foods.schemas import NutrientsOut
from app.foods.vocab import CulinaryRole
from app.nutrition.allergens import Exclusion, ExclusionCategory, Severity, TraceStatus, Verdict
from app.nutrition.nutrients import Nutrients
from app.optimizer.transform import Metric, Reason
from app.variants.explain import Kind


class _Snapshot(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True, allow_inf_nan=False)


class ExclusionIn(_Snapshot):
    category: ExclusionCategory
    severity: Severity
    term: str | None = Field(
        default=None, min_length=1, max_length=60, description="Only for category `other`"
    )
    relaxed: bool = Field(default=False, description="Only an intolerance can be relaxed")

    @model_validator(mode="after")
    def _valid(self) -> Self:
        self.to_exclusion()  # raises ValueError with the rule that was broken
        return self

    def to_exclusion(self) -> Exclusion:
        return Exclusion(self.category, self.severity, self.term, self.relaxed)


Exclusions = list[ExclusionIn]
MAX_EXCLUSIONS = 40


def to_exclusions(items: Exclusions) -> list[Exclusion]:
    return [e.to_exclusion() for e in items]


class MealTarget(_Snapshot):
    """One serving's target."""

    kcal: float = Field(ge=100, le=3000)
    protein_min_g: float = Field(ge=0, le=250)
    fat_g: float | None = Field(default=None, ge=0, le=300)
    carbs_g: float | None = Field(default=None, ge=0, le=500)


class SearchIn(_Snapshot):
    tags: list[str] = Field(default=[], max_length=10)
    max_total_minutes: int | None = Field(default=None, ge=1, le=1440)
    exclusions: Exclusions = Field(default=[], max_length=MAX_EXCLUSIONS)
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0, le=10_000)


class SaveIn(_Snapshot):
    label: str | None = Field(default=None, min_length=1, max_length=80)
    plan_id: uuid.UUID | None = Field(default=None, description="With `slot`: cook it there")
    slot: int | None = Field(default=None, ge=0, le=1000, description="The slot's position")

    @model_validator(mode="after")
    def _both(self) -> Self:
        if (self.plan_id is None) != (self.slot is None):
            raise ValueError("plan_id and slot go together")
        return self


class PersonalizeIn(_Snapshot):
    target: MealTarget
    exclusions: Exclusions = Field(
        default=[],
        max_length=MAX_EXCLUSIONS,
        description="Used without a stored profile with health-data consent (D8 fallback); "
        "ignored for a signed-in user who has one.",
    )
    save: SaveIn | None = Field(
        default=None,
        description="Save the proposal as the user's variant (sign-in required), optionally "
        "as the recipe of one of their plan slots. Only the meal target is stored with it.",
    )


class SubstitutionsIn(_Snapshot):
    ingredient: int = Field(ge=0, le=1000, description="The ingredient's `position`")
    exclusions: Exclusions = Field(default=[], max_length=MAX_EXCLUSIONS)
    limit: int = Field(default=5, ge=1, le=20)


def nutrients_out(n: Nutrients) -> NutrientsOut:
    r = n.rounded()
    return NutrientsOut(
        kcal=r.kcal, protein_g=r.protein_g, fat_g=r.fat_g, carbs_g=r.carbs_g, fiber_g=r.fiber_g
    )


class FoodRef(BaseModel):
    slug: str
    name_en: str
    name_pl: str


class ConflictOut(BaseModel):
    key: str
    verdict: Verdict
    optional: bool


class RecipeSummary(BaseModel):
    id: uuid.UUID
    slug: str | None
    title_en: str | None
    title_pl: str | None
    servings: int
    prep_minutes: int | None
    cook_minutes: int | None
    total_minutes: int | None
    difficulty: str | None
    tags: list[str]
    per_serving: NutrientsOut | None = Field(description="None until nutrition is computed")
    allergens: list[str]
    may_contain: list[str]
    trace_status: TraceStatus
    conflicts: list[ConflictOut] = Field(
        default=[],
        description="Ingredients the request's exclusions affect: `excluded` optional ones "
        "are left out when personalizing, `penalised` ones are dislikes. Recipes with an "
        "excluded required ingredient are not listed.",
    )


class RecipeList(BaseModel):
    items: list[RecipeSummary]
    total: int


class IngredientOut(BaseModel):
    key: str = Field(description="`<position>:<food slug>`, as used by personalize")
    position: int
    food: FoodRef
    amount_g: float = Field(description="For the whole recipe")
    per_serving_g: float
    display_amount: float | None
    display_unit: str | None
    culinary_role: CulinaryRole
    optional: bool
    prep_note: str | None
    allergens: list[str]
    may_contain: list[str]
    trace_status: TraceStatus


class NutritionOut(BaseModel):
    total: NutrientsOut
    per_serving: NutrientsOut
    total_grams: float


class RecipeDetail(RecipeSummary):
    instructions_en: list[str]
    instructions_pl: list[str]
    equipment: list[str]
    fridge_days: int | None
    freezer_friendly: bool
    meal_prep_score: int | None
    ingredients: list[IngredientOut]
    nutrition: NutritionOut


class ChangeReason(StrEnum):
    """Why an amount changed: the engine's reasons plus removal for an exclusion."""

    RAISE_PROTEIN = Reason.RAISE_PROTEIN.value
    CUT_CALORIES = Reason.CUT_CALORIES.value
    ADD_CALORIES = Reason.ADD_CALORIES.value
    LOWER_FAT = Reason.LOWER_FAT.value
    ADJUST_CARBS = Reason.ADJUST_CARBS.value
    MORE_VOLUME = Reason.MORE_VOLUME.value
    REMOVED_OPTIONAL = Reason.REMOVED_OPTIONAL.value
    ROUNDING = Reason.ROUNDING.value
    EXCLUDED = "excluded"  # an optional ingredient the user's exclusions rule out


class ChangeOut(BaseModel):
    key: str
    original_g: float
    grams: float
    reason: ChangeReason


class SwapOut(BaseModel):
    original_key: str
    replacement_key: str
    food: FoodRef
    grams: float = Field(description="Amount doing the same job, before adjusting to the target")


class ProposedIngredient(BaseModel):
    key: str = Field(description="The original ingredient's key")
    position: int
    food: FoodRef = Field(description="The food used in the proposal (the substitute if swapped)")
    original_food: str
    original_g: float = Field(description="Per serving")
    grams: float = Field(description="Per serving in the proposal; 0 when removed")
    removed: bool
    swapped: bool


class MissOut(BaseModel):
    metric: Metric
    target: float
    actual: float


class ExplanationOut(BaseModel):
    """One change in plain words ("Why did Donut change this?")."""

    key: str = Field(description="The ingredient's key")
    kind: Kind
    message: str
    delta: NutrientsOut = Field(description="The change's effect on one serving")
    reason: ChangeReason | None = Field(description="For `amount` changes")


class PersonalizeOut(BaseModel):
    """A proposal for one serving. Nothing is stored unless the request asks to save it."""

    recipe_id: uuid.UUID
    ingredients: list[ProposedIngredient]
    changes: list[ChangeOut]
    swaps: list[SwapOut]
    original_nutrition: NutrientsOut
    nutrition: NutrientsOut
    on_target: bool
    misses: list[MissOut]
    explanations: list[ExplanationOut] = Field(default=[], description="Every change, in words")
    variant_id: uuid.UUID | None = Field(default=None, description="Set when saved")


class SubstitutionOption(BaseModel):
    food: FoodRef
    grams: float = Field(description="Per serving, scaled to do the same job")
    same_group: bool
    disliked: bool
    delta: NutrientsOut = Field(description="Substitute minus original, per serving")
    score: float = Field(description="Lower ranks first")


class SubstitutionsOut(BaseModel):
    key: str
    position: int
    food: FoodRef
    grams: float = Field(description="Per serving")
    culinary_role: CulinaryRole
    excluded: bool = Field(description="The request's exclusions rule this ingredient out")
    remove: bool = Field(description="Excluded and optional: leaving it out is the fix")
    options: list[SubstitutionOption]


class BlockedDetail(BaseModel):
    message: str
    must_substitute: list[str] = Field(
        default=[], description="Keys of the excluded required ingredients"
    )


class BlockedOut(BaseModel):
    detail: BlockedDetail
