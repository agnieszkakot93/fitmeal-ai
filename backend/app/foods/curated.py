"""The hand-curated ingredient list (``data/foods/curated.yaml``).

The curated file owns everything *about* an ingredient — names, aliases,
category, allergens and "may contain" traces, culinary roles, portion
weights, densities, package sizes — and says where its nutrition comes from:
a USDA FoodData Central record (``fdc``) or a product label (``nutrition``).
Items with neither are kept in the file as ``pending`` and skipped by the
importer.

Every entry also carries its provenance: a ``review`` status (only a named
human sets ``verified``) and a ``traces`` status saying whether its "may
contain" list is known, and from which source. Both default to the cautious
side: review ``draft``, traces ``unknown``.
"""

from __future__ import annotations

import datetime
from enum import StrEnum
from pathlib import Path
from typing import Self

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.foods.vocab import CulinaryRole, FoodCategory
from app.nutrition.allergens import Allergen, Origin, TraceStatus
from app.nutrition.units import UNITS, UnitKind


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Names(_Strict):
    en: str
    pl: str


class Aliases(_Strict):
    en: list[str] = []
    pl: list[str] = []


class FdcRef(_Strict):
    fdc_id: int | None = None
    description: str | None = None

    @model_validator(mode="after")
    def _one_key(self) -> Self:
        if (self.fdc_id is None) == (self.description is None):
            raise ValueError("fdc needs exactly one of fdc_id or description")
        return self


class LabelNutrition(_Strict):
    """Per 100 g, EU label convention (carbs exclude fiber)."""

    kcal: float = Field(ge=0)
    protein_g: float = Field(ge=0)
    fat_g: float = Field(ge=0)
    carbs_g: float = Field(ge=0)
    fiber_g: float = Field(ge=0)
    source_ref: str


class ReviewStatus(StrEnum):
    DRAFT = "draft"
    AUTO_CHECKED = "auto_checked"  # passed automated checks; no human has signed off
    VERIFIED = "verified"  # a named human checked the whole entry; never set by an agent


class Review(_Strict):
    status: ReviewStatus = ReviewStatus.DRAFT
    by: str | None = Field(default=None, pattern=r"^[A-Z]{2,4}$", description="initials")
    date: datetime.date | None = None

    @model_validator(mode="after")
    def _signed(self) -> Self:
        if self.status is ReviewStatus.VERIFIED and (self.by is None or self.date is None):
            raise ValueError("a verified review needs `by` (initials) and `date`")
        return self


class TraceSourceType(StrEnum):
    LABEL = "label"  # a product label's "may contain" statement
    POLICY = "policy"  # a rule of the approved generic-food policy (docs/data/TRACE_POLICY.md)


class TraceSource(_Strict):
    type: TraceSourceType
    ref: str = Field(min_length=1)


class Traces(_Strict):
    status: TraceStatus = TraceStatus.UNKNOWN
    source: TraceSource | None = None

    @model_validator(mode="after")
    def _sourced(self) -> Self:
        if self.status is TraceStatus.UNKNOWN and self.source is not None:
            raise ValueError("unknown traces have no source; use none_declared or declared")
        if self.status is not TraceStatus.UNKNOWN and self.source is None:
            raise ValueError(f"traces {self.status.value!r} need a source")
        return self


class CuratedFood(_Strict):
    slug: str = Field(pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    name: Names
    aliases: Aliases = Aliases()
    category: FoodCategory
    origin: Origin
    allergens: list[Allergen] = []
    # "may contain" / trace declarations, kept apart from what the food contains
    may_contain: list[Allergen] = []
    traces: Traces = Traces()
    review: Review = Review()
    derived_from: list[str] = []
    culinary_roles: list[CulinaryRole] = Field(min_length=1)
    substitution_groups: list[str] = []
    density_g_per_ml: float | None = Field(default=None, gt=0)
    portions: dict[str, float] = {}
    packages_g: list[float] = []
    fdc: FdcRef | None = None
    nutrition: LabelNutrition | None = None

    @model_validator(mode="after")
    def _check(self) -> Self:
        if self.fdc is not None and self.nutrition is not None:
            raise ValueError(f"{self.slug}: use either fdc or nutrition, not both")
        both = set(self.allergens) & set(self.may_contain)
        if both:
            raise ValueError(f"{self.slug}: {sorted(both)} listed as both allergen and trace")
        if self.traces.status is TraceStatus.DECLARED and not self.may_contain:
            raise ValueError(f"{self.slug}: declared traces need a non-empty may_contain")
        if self.traces.status is not TraceStatus.DECLARED and self.may_contain:
            raise ValueError(
                f"{self.slug}: may_contain needs traces status 'declared', "
                f"not {self.traces.status.value!r}"
            )
        for unit, grams in self.portions.items():
            if unit not in UNITS:
                raise ValueError(f"{self.slug}: unknown portion unit {unit!r}")
            if UNITS[unit].kind is UnitKind.MASS:
                raise ValueError(f"{self.slug}: portion unit {unit!r} is already a mass unit")
            if grams <= 0:
                raise ValueError(f"{self.slug}: portion {unit!r} must be positive")
        if any(size <= 0 for size in self.packages_g):
            raise ValueError(f"{self.slug}: package sizes must be positive")
        return self

    @property
    def pending(self) -> bool:
        return self.fdc is None and self.nutrition is None


class CuratedFile(_Strict):
    foods: list[CuratedFood]

    @model_validator(mode="after")
    def _cross_refs(self) -> Self:
        slugs = [f.slug for f in self.foods]
        dupes = {s for s in slugs if slugs.count(s) > 1}
        if dupes:
            raise ValueError(f"duplicate slugs: {sorted(dupes)}")
        known = set(slugs)
        for food in self.foods:
            missing = [p for p in food.derived_from if p not in known]
            if missing:
                raise ValueError(f"{food.slug}: derived_from unknown foods {missing}")
        return self


def load_curated(path: Path) -> CuratedFile:
    with path.open(encoding="utf-8") as fh:
        return CuratedFile.model_validate(yaml.safe_load(fh))
