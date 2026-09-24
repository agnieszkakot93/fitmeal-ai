"""Curated list + FDC data → rows in the food tables.

Two steps so the matching logic can be tested without a database:

1. :func:`resolve` pairs every curated food with its nutrition source and
   produces a report of what could not be matched.
2. :func:`apply` upserts the resolved foods (idempotent; safe to re-run).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.text import fold
from app.foods.curated import CuratedFile, CuratedFood, ReviewStatus
from app.foods.fdc import FdcIndex
from app.foods.lint import allergen_problems
from app.foods.models import FoodAlias, FoodDerivation, FoodItem, FoodPackage, FoodPortion
from app.nutrition.allergens import (
    Allergen,
    TraceStatus,
    effective_allergens,
    effective_trace_status,
    effective_traces,
)
from app.nutrition.nutrients import Nutrients, energy_is_consistent


@dataclass(frozen=True, slots=True)
class ResolvedFood:
    curated: CuratedFood
    nutrients: Nutrients
    water_g: float | None
    source: str
    source_ref: str
    effective_allergens: frozenset[Allergen]
    effective_may_contain: frozenset[Allergen] = frozenset()
    # unknown unless the food and everything it is derived from say otherwise
    effective_trace_status: TraceStatus = TraceStatus.UNKNOWN


@dataclass
class ImportReport:
    resolved: list[ResolvedFood] = field(default_factory=list)
    pending: list[str] = field(default_factory=list)
    # slug → close FDC descriptions to help fix the curated entry
    unmatched: dict[str, list[str]] = field(default_factory=dict)
    energy_warnings: list[str] = field(default_factory=list)
    # contradictions between origin/name and declared allergens; block writing
    allergen_problems: list[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = [
            f"resolved: {len(self.resolved)}",
            f"pending (no nutrition source yet): {len(self.pending)}",
            f"unmatched in FDC: {len(self.unmatched)}",
        ]
        for slug, suggestions in sorted(self.unmatched.items()):
            lines.append(f"  - {slug}")
            lines.extend(f"      ? {s}" for s in suggestions)
        if self.energy_warnings:
            lines.append(f"energy/macro mismatches: {len(self.energy_warnings)}")
            lines.extend(f"  - {w}" for w in self.energy_warnings)
        if self.allergen_problems:
            lines.append(
                f"allergen contradictions (fix before importing): {len(self.allergen_problems)}"
            )
            lines.extend(f"  - {p}" for p in self.allergen_problems)
        return "\n".join(lines)


def resolve(curated: CuratedFile, index: FdcIndex | None) -> ImportReport:
    report = ImportReport()
    derived_from = {f.slug: f.derived_from for f in curated.foods}
    allergens = effective_allergens({f.slug: f.allergens for f in curated.foods}, derived_from)
    traces = effective_traces(
        {f.slug: f.may_contain for f in curated.foods}, derived_from, allergens
    )
    trace_status = effective_trace_status(
        {f.slug: f.traces.status for f in curated.foods}, derived_from, traces
    )
    report.allergen_problems = allergen_problems(curated)

    for food in curated.foods:
        if food.pending:
            report.pending.append(food.slug)
            continue

        if food.nutrition is not None:
            n = food.nutrition
            nutrients = Nutrients(n.kcal, n.protein_g, n.fat_g, n.carbs_g, n.fiber_g)
            resolved = ResolvedFood(
                food,
                nutrients,
                None,
                "label",
                n.source_ref,
                allergens[food.slug],
                traces[food.slug],
                trace_status[food.slug],
            )
        else:
            assert food.fdc is not None
            match = (
                index.find(fdc_id=food.fdc.fdc_id, description=food.fdc.description)
                if index is not None
                else None
            )
            if match is None:
                report.unmatched[food.slug] = (
                    index.suggest(food.fdc.description)
                    if index is not None and food.fdc.description
                    else []
                )
                continue
            resolved = ResolvedFood(
                food,
                match.nutrients,
                match.water_g,
                "usda_fdc",
                str(match.fdc_id),
                allergens[food.slug],
                traces[food.slug],
                trace_status[food.slug],
            )

        if not energy_is_consistent(resolved.nutrients):
            report.energy_warnings.append(f"{food.slug}: {resolved.nutrients}")
        report.resolved.append(resolved)

    return report


async def apply(session: AsyncSession, resolved: list[ResolvedFood]) -> None:
    slugs = [r.curated.slug for r in resolved]
    existing = {
        item.slug: item
        for item in await session.scalars(select(FoodItem).where(FoodItem.slug.in_(slugs)))
    }

    items: dict[str, FoodItem] = {}
    for r in resolved:
        c = r.curated
        item = existing.get(c.slug) or FoodItem(slug=c.slug)
        item.name_en = c.name.en
        item.name_pl = c.name.pl
        item.category = c.category.value
        item.origin = c.origin.value
        item.kcal = r.nutrients.kcal
        item.protein_g = r.nutrients.protein_g
        item.fat_g = r.nutrients.fat_g
        item.carbs_g = r.nutrients.carbs_g
        item.fiber_g = r.nutrients.fiber_g
        item.water_g = r.water_g
        item.density_g_per_ml = c.density_g_per_ml
        item.allergens = sorted(a.value for a in c.allergens)
        item.effective_allergens = sorted(a.value for a in r.effective_allergens)
        item.may_contain = sorted(a.value for a in c.may_contain)
        item.effective_may_contain = sorted(a.value for a in r.effective_may_contain)
        item.trace_status = c.traces.status.value
        item.effective_trace_status = r.effective_trace_status.value
        item.culinary_roles = [role.value for role in c.culinary_roles]
        item.substitution_groups = list(c.substitution_groups)
        item.source = r.source
        item.source_ref = r.source_ref
        item.reviewed = c.review.status is ReviewStatus.VERIFIED
        session.add(item)
        items[c.slug] = item
    await session.flush()

    # Child rows are replaced wholesale; deleting first keeps unique keys happy.
    ids = [item.id for item in items.values()]
    for child in (FoodAlias, FoodPortion, FoodPackage, FoodDerivation):
        await session.execute(delete(child).where(child.food_id.in_(ids)))
    for r in resolved:
        c = r.curated
        food_id = items[c.slug].id
        session.add_all(_aliases(c, food_id))
        session.add_all(
            FoodPortion(food_id=food_id, unit=u, grams=g) for u, g in sorted(c.portions.items())
        )
        session.add_all(FoodPackage(food_id=food_id, size_g=s) for s in c.packages_g)

    parent_ids = dict((await session.execute(select(FoodItem.slug, FoodItem.id))).all())
    for r in resolved:
        for parent in r.curated.derived_from:
            # A parent that is still pending has no row yet; its allergens,
            # traces and trace status are already in the effective columns above.
            if parent in parent_ids:
                session.add(
                    FoodDerivation(food_id=items[r.curated.slug].id, parent_id=parent_ids[parent])
                )
    await session.flush()


def _aliases(c: CuratedFood, food_id: uuid.UUID) -> list[FoodAlias]:
    seen: set[tuple[str, str]] = set()
    rows = []
    for lang, names in (("en", [c.name.en, *c.aliases.en]), ("pl", [c.name.pl, *c.aliases.pl])):
        for alias in names:
            key = (lang, fold(alias))
            if key in seen:
                continue
            seen.add(key)
            rows.append(FoodAlias(food_id=food_id, lang=lang, alias=alias, alias_folded=key[1]))
    return rows
