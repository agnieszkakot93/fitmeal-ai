"""The planner on the real catalog (``data/recipes/catalog.yaml``).

``fixtures/planner/catalog.json`` is a frozen extract of the catalog with
per-serving nutrition from the committed FDC snapshot and each ingredient's
allergen facts, so the planner tests run without a database.
:func:`test_extract_matches_catalog` rebuilds it from the database and fails
if it drifts; run it with ``DONUT_WRITE_PLANNER_FIXTURE=1`` to rewrite the file
after a catalog or food data change.
"""

from __future__ import annotations

import dataclasses
import json
import os
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.foods import importer
from app.foods.curated import load_curated
from app.foods.fdc import load_fdc_dirs
from app.nutrition.allergens import (
    Allergen,
    Exclusion,
    ExclusionCategory,
    IngredientAllergens,
    Origin,
    Severity,
    TraceStatus,
)
from app.nutrition.nutrients import Nutrients
from app.planner.inputs import Candidate, MealSlot, MealType, Profile
from app.planner.plan import plan, verify
from app.planner.result import Action, Infeasible, Plan
from app.planner.solve import SolverConfig
from app.plans.repository import to_candidate
from app.recipes import catalog, repository
from app.recipes.models import Recipe
from app.recipes.safety import CheckLine
from tests.test_foods_db import CURATED, ROOT

SNAPSHOT = ROOT / "data" / "foods" / "fdc_snapshot"
CATALOG = ROOT / "data" / "recipes" / "catalog.yaml"
EXTRACT = Path(__file__).parent / "fixtures" / "planner" / "catalog.json"

CONFIG = SolverConfig(deterministic_time=1.0, time_limit_s=30.0, workers=1, seed=0)

TYPICAL = Profile(
    daily_kcal=2000,
    protein_min_g=120,
    meals=(
        MealSlot("breakfast", MealType.BREAKFAST, 0.3),
        MealSlot("lunch", MealType.LUNCH, 0.35),
        MealSlot("dinner", MealType.DINNER, 0.35),
    ),
    days=7,
    prep_days=2,
    max_minutes=60,
    equipment=frozenset({"oven", "blender"}),
)


def _line_to_json(line: CheckLine) -> dict[str, Any]:
    a = line.allergens
    return {
        "key": line.key,
        "optional": line.optional,
        "origin": a.origin.value,
        "contains": sorted(a.contains),
        "may_contain": sorted(a.may_contain),
        "trace_status": a.trace_status.value,
        "names": list(a.names),
    }


def _line_from_json(raw: dict[str, Any]) -> CheckLine:
    return CheckLine(
        raw["key"],
        IngredientAllergens(
            origin=Origin(raw["origin"]),
            contains=frozenset(Allergen(x) for x in raw["contains"]),
            may_contain=frozenset(Allergen(x) for x in raw["may_contain"]),
            names=tuple(raw["names"]),
            trace_status=TraceStatus(raw["trace_status"]),
        ),
        raw["optional"],
    )


def to_json(c: Candidate) -> dict[str, Any]:
    n = c.per_serving
    return {
        "id": c.id,
        "tags": sorted(c.tags),
        "per_serving": {
            "kcal": round(n.kcal, 1),
            "protein_g": round(n.protein_g, 1),
            "fat_g": round(n.fat_g, 1),
            "carbs_g": round(n.carbs_g, 1),
            "fiber_g": round(n.fiber_g, 1),
        },
        "servings": c.servings,
        "fridge_days": c.fridge_days,
        "freezer_friendly": c.freezer_friendly,
        "meal_prep_score": c.meal_prep_score,
        "total_minutes": c.total_minutes,
        "equipment": sorted(c.equipment),
        "ingredient_ids": sorted(c.ingredient_ids),
        "allergen_lines": [_line_to_json(line) for line in c.allergen_lines],
    }


def from_json(raw: dict[str, Any]) -> Candidate:
    return Candidate(
        id=raw["id"],
        tags=frozenset(raw["tags"]),
        per_serving=Nutrients(**raw["per_serving"]),
        servings=raw["servings"],
        fridge_days=raw["fridge_days"],
        freezer_friendly=raw["freezer_friendly"],
        meal_prep_score=raw["meal_prep_score"],
        total_minutes=raw["total_minutes"],
        equipment=frozenset(raw["equipment"]),
        allergen_lines=tuple(_line_from_json(x) for x in raw["allergen_lines"]),
        ingredient_ids=frozenset(raw["ingredient_ids"]),
    )


def load_extract() -> list[Candidate]:
    with EXTRACT.open(encoding="utf-8") as fh:
        return [from_json(r) for r in json.load(fh)["recipes"]]


async def test_extract_matches_catalog(db_session: AsyncSession) -> None:
    report = importer.resolve(load_curated(CURATED), load_fdc_dirs([SNAPSHOT]))
    await importer.apply(db_session, report.resolved)
    await catalog.apply(db_session, catalog.load_catalog(CATALOG))
    await db_session.commit()
    ids = await db_session.scalars(
        select(Recipe.id).where(Recipe.slug.is_not(None)).order_by(Recipe.slug)
    )
    live = []
    for recipe_id in list(ids):
        recipe = await repository.get(db_session, recipe_id)
        assert recipe is not None
        live.append(to_json(to_candidate(recipe)))
    if os.environ.get("DONUT_WRITE_PLANNER_FIXTURE"):
        EXTRACT.parent.mkdir(parents=True, exist_ok=True)
        rows = ",\n".join(json.dumps(r, ensure_ascii=False) for r in live)
        EXTRACT.write_text('{"recipes": [\n' + rows + "\n]}\n", encoding="utf-8")
    with EXTRACT.open(encoding="utf-8") as fh:
        frozen = json.load(fh)["recipes"]
    assert frozen == live, "planner fixture is stale: rerun with DONUT_WRITE_PLANNER_FIXTURE=1"


def _solve(profile: Profile) -> Plan:
    candidates = load_extract()
    result = plan(candidates, profile, CONFIG)
    assert isinstance(result, Plan), result.message
    assert verify(result, candidates, profile) == []
    return result


def test_typical_week_is_found() -> None:
    result = _solve(TYPICAL)
    assert len(result.days) == 7
    assert result.notices == ()
    lo, hi = TYPICAL.kcal_window
    for day in result.days:
        assert lo <= day.totals.kcal <= hi
        assert day.totals.protein_g >= 120
    # cook once for 2 days: some meals come from a batch
    assert any(m.from_batch for m in result.meals)


def test_typical_week_is_deterministic() -> None:
    assert _solve(TYPICAL) == _solve(TYPICAL)


def _with(**changes: Any) -> Profile:
    return dataclasses.replace(TYPICAL, **changes)


def test_milk_intolerance_week_has_no_milk() -> None:
    profile = _with(exclusions=(Exclusion(ExclusionCategory.MILK, Severity.INTOLERANCE),))
    result = _solve(profile)
    by_id = {c.id: c for c in load_extract()}
    for meal in result.meals:
        for line in by_id[meal.recipe_id].allergen_lines:
            if line.key not in meal.leave_out:
                assert Allergen.MILK not in line.allergens.contains, (meal.recipe_id, line.key)


def test_milk_allergy_is_blocked_by_unknown_traces() -> None:
    # Most catalog foods have no checked trace data yet, and an allergy
    # excludes unknown traces (PRD §7): the report must say so, not crash.
    profile = _with(exclusions=(Exclusion(ExclusionCategory.MILK, Severity.ALLERGY),))
    result = plan(load_extract(), profile, CONFIG)
    assert isinstance(result, Infeasible)
    assert result.blockers
    assert all("milk" in b.message for b in result.blockers)
    assert {s.action for s in result.suggestions} == {Action.ADD_RECIPES}


def test_vegan_lactose_free_quick_week() -> None:
    profile = _with(
        days=5,
        protein_min_g=90,
        max_minutes=30,
        exclusions=(
            Exclusion(ExclusionCategory.MEAT, Severity.DISLIKE),
            Exclusion(ExclusionCategory.MILK, Severity.INTOLERANCE),
        ),
    )
    result = plan(load_extract(), profile, CONFIG)
    # either a plan that passes every hard check, or a report naming the blocker
    if isinstance(result, Plan):
        assert verify(result, load_extract(), profile) == []
    else:
        assert result.blockers and result.suggestions
