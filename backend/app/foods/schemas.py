from __future__ import annotations

from pydantic import BaseModel, Field

from app.foods.models import FoodItem
from app.nutrition.allergens import TraceStatus


class NutrientsOut(BaseModel):
    kcal: float
    protein_g: float
    fat_g: float
    carbs_g: float = Field(description="Available carbohydrate, excluding fiber (EU label style)")
    fiber_g: float


class FoodSummary(BaseModel):
    slug: str
    name_en: str
    name_pl: str
    category: str
    per_100g: NutrientsOut

    @classmethod
    def of(cls, item: FoodItem) -> FoodSummary:
        return cls(
            slug=item.slug,
            name_en=item.name_en,
            name_pl=item.name_pl,
            category=item.category,
            per_100g=NutrientsOut(
                kcal=item.kcal,
                protein_g=item.protein_g,
                fat_g=item.fat_g,
                carbs_g=item.carbs_g,
                fiber_g=item.fiber_g,
            ),
        )


class FoodSearchHit(FoodSummary):
    score: float


class FoodDetail(FoodSummary):
    origin: str
    allergens: list[str] = Field(description="Effective allergens, including inherited ones")
    may_contain: list[str] = Field(
        description='Effective "may contain" (trace) allergens, including inherited ones. '
        "Never repeats an entry of `allergens`."
    )
    trace_status: TraceStatus = Field(
        description='Whether the "may contain" data is known, including inherited status. '
        "`unknown`: nobody has checked this food or something it is made from, so any "
        "allergen could be a trace (not the same as none); an ALLERGY exclusion never "
        "allows it. `none_declared`: checked, no traces. `declared`: checked, listed in "
        "`may_contain`."
    )
    culinary_roles: list[str]
    substitution_groups: list[str]
    density_g_per_ml: float | None
    portions_g: dict[str, float]
    packages_g: list[float]
    aliases: dict[str, list[str]]
    source: str
    source_ref: str | None

    @classmethod
    def of(cls, item: FoodItem) -> FoodDetail:
        aliases: dict[str, list[str]] = {}
        for a in item.aliases:
            aliases.setdefault(a.lang, []).append(a.alias)
        return cls(
            **FoodSummary.of(item).model_dump(),
            origin=item.origin,
            allergens=item.effective_allergens,
            may_contain=item.effective_may_contain,
            trace_status=TraceStatus(item.effective_trace_status),
            culinary_roles=item.culinary_roles,
            substitution_groups=item.substitution_groups,
            density_g_per_ml=item.density_g_per_ml,
            portions_g={p.unit: p.grams for p in item.portions},
            packages_g=sorted(p.size_g for p in item.packages),
            aliases=aliases,
            source=item.source,
            source_ref=item.source_ref,
        )
