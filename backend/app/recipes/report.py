"""Per-serving nutrition report for stored recipes, with plausibility flags.

A sanity check for the catalog against real food data: it flags numbers a
cook or dietitian would question, not hard errors.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.foods.models import FoodItem
from app.nutrition.nutrients import Nutrients
from app.recipes import repository
from app.recipes.models import Recipe, RecipeIngredient

MEALS = {"breakfast", "lunch", "dinner"}
# protein a recipe needs to earn its high_protein tag
HIGH_PROTEIN_MEAL_G = 25
HIGH_PROTEIN_SNACK_G = 15


@dataclass(frozen=True, slots=True)
class Row:
    slug: str
    tags: list[str]
    per_serving: Nutrients
    grams_per_serving: float
    flags: list[str]


def flags_for(tags: list[str], n: Nutrients, grams: float) -> list[str]:
    found = []
    meal = bool(MEALS & set(tags))
    if meal and n.kcal < 200:
        found.append("low kcal for a meal")
    if n.kcal > 1000:
        found.append("over 1000 kcal")
    if n.kcal > 0 and n.fat_g * 9 / n.kcal > 0.45:
        found.append("fat over 45% of kcal")
    if "high_protein" in tags:
        minimum = HIGH_PROTEIN_MEAL_G if meal else HIGH_PROTEIN_SNACK_G
        if n.protein_g < minimum:
            found.append(f"tagged high_protein but under {minimum} g")
    if meal and n.protein_g < 10:
        found.append("under 10 g protein")
    if grams > 800 and "soup" not in tags:  # broth is mostly water
        found.append("portion over 800 g")
    return found


async def build(session: AsyncSession) -> list[Row]:
    recipes = await session.scalars(
        select(Recipe)
        .where(Recipe.slug.is_not(None))
        .order_by(Recipe.slug)
        .options(
            selectinload(Recipe.ingredients)
            .selectinload(RecipeIngredient.food)
            .selectinload(FoodItem.portions)
        )
    )
    rows = []
    for recipe in recipes:
        result = repository.compute_nutrition(recipe)
        n = result.per_serving
        grams = result.total_grams / recipe.servings
        rows.append(Row(recipe.slug or "", recipe.tags, n, grams, flags_for(recipe.tags, n, grams)))
    return rows


def render(rows: list[Row]) -> str:
    header = f"{'recipe':<36} {'kcal':>5} {'P':>5} {'F':>5} {'C':>5} {'g':>5}  flags"
    lines = [header, "-" * len(header)]
    for r in rows:
        n = r.per_serving
        lines.append(
            f"{r.slug:<36} {n.kcal:>5.0f} {n.protein_g:>5.1f} {n.fat_g:>5.1f} "
            f"{n.carbs_g:>5.1f} {r.grams_per_serving:>5.0f}  {'; '.join(r.flags)}"
        )
    flagged = sum(1 for r in rows if r.flags)
    lines.append(f"\n{len(rows)} recipes, {flagged} flagged (per serving; P/F/C in grams)")
    return "\n".join(lines)
