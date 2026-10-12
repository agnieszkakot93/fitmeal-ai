"""The Donut-owned recipe catalog (``data/recipes/catalog.yaml``).

Catalog recipes are written by Donut, so they are the only public recipes
(PRD §8.1). The file gives each ingredient as an amount in a kitchen unit; the
importer converts it to grams with the food's portion weights and density,
and computes nutrition from that. Nutrition is never typed in the file.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.foods.curated import CuratedFile, Names, Review
from app.foods.models import FoodItem
from app.foods.vocab import CulinaryRole
from app.nutrition.units import UNITS, FoodUnitData, to_grams
from app.recipes import repository
from app.recipes.models import (
    Difficulty,
    PublicUsageStatus,
    Recipe,
    RecipeIngredient,
    RecipeSource,
    SourceType,
)


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Steps(_Strict):
    en: list[str] = Field(min_length=1)
    pl: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def _parallel(self) -> Self:
        if len(self.en) != len(self.pl):
            raise ValueError("en and pl need the same number of steps")
        return self


class Storage(_Strict):
    fridge_days: int = Field(ge=0)
    freezer_friendly: bool = False


class CatalogIngredient(_Strict):
    food: str
    amount: float = Field(gt=0)
    unit: str = "g"
    # defaults to the food's first culinary role
    role: CulinaryRole | None = None
    optional: bool = False

    @model_validator(mode="after")
    def _unit(self) -> Self:
        if self.unit not in UNITS:
            raise ValueError(f"{self.food}: unknown unit {self.unit!r}")
        return self


class CatalogRecipe(_Strict):
    slug: str = Field(pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    title: Names
    servings: int = Field(ge=1)
    prep_minutes: int = Field(ge=0)
    cook_minutes: int = Field(ge=0)
    difficulty: Difficulty
    tags: list[str] = []
    equipment: list[str] = []
    storage: Storage
    meal_prep_score: int = Field(ge=0, le=100)
    ingredients: list[CatalogIngredient] = Field(min_length=1)
    steps: Steps
    review: Review = Review()


class CatalogFile(_Strict):
    recipes: list[CatalogRecipe]

    @model_validator(mode="after")
    def _unique(self) -> Self:
        slugs = [r.slug for r in self.recipes]
        dupes = {s for s in slugs if slugs.count(s) > 1}
        if dupes:
            raise ValueError(f"duplicate slugs: {sorted(dupes)}")
        return self


def load_catalog(path: Path) -> CatalogFile:
    with path.open(encoding="utf-8") as fh:
        return CatalogFile.model_validate(yaml.safe_load(fh))


def check_against_foods(catalog: CatalogFile, curated: CuratedFile) -> list[str]:
    """Problems that only show with the food list: unknown, pending or unconvertible foods."""
    foods = {f.slug: f for f in curated.foods}
    problems = []
    for recipe in catalog.recipes:
        for line in recipe.ingredients:
            food = foods.get(line.food)
            if food is None:
                problems.append(f"{recipe.slug}: unknown food {line.food!r}")
                continue
            if food.pending:
                problems.append(f"{recipe.slug}: {line.food!r} has no nutrition source yet")
            units = FoodUnitData(food.density_g_per_ml, food.portions)
            try:
                to_grams(line.amount, line.unit, units)
            except ValueError as exc:
                problems.append(f"{recipe.slug}: {line.food} {line.unit}: {exc}")
    return problems


@dataclass
class CatalogReport:
    written: list[str] = field(default_factory=list)
    # recipe slug → foods missing from the database (e.g. not imported yet)
    skipped: dict[str, list[str]] = field(default_factory=dict)

    def summary(self) -> str:
        lines = [f"written: {len(self.written)} recipes, skipped: {len(self.skipped)}"]
        lines += [f"  skipped {slug}: missing {foods}" for slug, foods in self.skipped.items()]
        return "\n".join(lines)


async def apply(session: AsyncSession, catalog: CatalogFile) -> CatalogReport:
    """Insert or update every catalog recipe whose foods are all in the database."""
    slugs = {line.food for r in catalog.recipes for line in r.ingredients}
    foods = {
        f.slug: f
        for f in await session.scalars(
            select(FoodItem)
            .where(FoodItem.slug.in_(slugs))
            .options(selectinload(FoodItem.portions))
        )
    }
    existing = {
        r.slug: r
        for r in await session.scalars(
            select(Recipe)
            .where(Recipe.slug.in_([r.slug for r in catalog.recipes]))
            .options(selectinload(Recipe.ingredients))
        )
    }

    report = CatalogReport()
    for entry in catalog.recipes:
        missing = sorted({i.food for i in entry.ingredients} - foods.keys())
        if missing:
            report.skipped[entry.slug] = missing
            continue
        recipe = existing.get(entry.slug)
        if recipe is None:
            recipe = Recipe(
                slug=entry.slug,
                source=RecipeSource(
                    type=SourceType.CATALOG, public_usage_status=PublicUsageStatus.PUBLIC
                ),
            )
            session.add(recipe)
        else:
            # flush the removals first so new rows can reuse (recipe_id, position)
            recipe.ingredients.clear()
            await session.flush()
        _fill(recipe, entry, foods)
        repository.refresh_nutrition(recipe)
        repository.refresh_allergens(recipe)
        report.written.append(entry.slug)
    await session.flush()
    return report


def _fill(recipe: Recipe, entry: CatalogRecipe, foods: dict[str, FoodItem]) -> None:
    recipe.title_en = entry.title.en
    recipe.title_pl = entry.title.pl
    recipe.instructions_en = list(entry.steps.en)
    recipe.instructions_pl = list(entry.steps.pl)
    recipe.servings = entry.servings
    recipe.prep_minutes = entry.prep_minutes
    recipe.cook_minutes = entry.cook_minutes
    recipe.difficulty = entry.difficulty.value
    recipe.tags = list(entry.tags)
    recipe.equipment = list(entry.equipment)
    recipe.fridge_days = entry.storage.fridge_days
    recipe.freezer_friendly = entry.storage.freezer_friendly
    recipe.meal_prep_score = entry.meal_prep_score
    recipe.ingredients = [
        _ingredient(position, line, foods[line.food])
        for position, line in enumerate(entry.ingredients)
    ]


def _ingredient(position: int, line: CatalogIngredient, food: FoodItem) -> RecipeIngredient:
    units = FoodUnitData(food.density_g_per_ml, {p.unit: p.grams for p in food.portions})
    in_grams = line.unit == "g"
    return RecipeIngredient(
        position=position,
        food=food,
        amount_g=to_grams(line.amount, line.unit, units),
        display_amount=None if in_grams else line.amount,
        display_unit=None if in_grams else line.unit,
        culinary_role=(line.role or food.culinary_roles[0]),
        optional=line.optional,
    )
