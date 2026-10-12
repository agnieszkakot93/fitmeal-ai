from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.foods.models import FoodItem
from app.foods.repository import to_facts
from app.foods.vocab import CulinaryRole
from app.nutrition.calc import IngredientLine, RecipeNutrition, calculate
from app.optimizer.transform import Line
from app.recipes.models import Recipe, RecipeIngredient


async def get(session: AsyncSession, recipe_id: uuid.UUID) -> Recipe | None:
    """A recipe with its ingredients and their foods (with portions) loaded."""
    stmt = (
        select(Recipe)
        .where(Recipe.id == recipe_id)
        .options(
            selectinload(Recipe.ingredients)
            .selectinload(RecipeIngredient.food)
            .selectinload(FoodItem.portions)
        )
    )
    return (await session.scalars(stmt)).one_or_none()


def compute_nutrition(recipe: Recipe) -> RecipeNutrition:
    """Nutrition from the ingredient weights; needs ingredients and foods loaded (``get``)."""
    lines = [IngredientLine(to_facts(i.food), i.amount_g, "g") for i in recipe.ingredients]
    return calculate(lines, recipe.servings)


def refresh_nutrition(recipe: Recipe) -> RecipeNutrition:
    """Recompute and store the cached totals. Call after any ingredient change."""
    result = compute_nutrition(recipe)
    total = result.total
    recipe.kcal = total.kcal
    recipe.protein_g = total.protein_g
    recipe.fat_g = total.fat_g
    recipe.carbs_g = total.carbs_g
    recipe.fiber_g = total.fiber_g
    recipe.total_grams = result.total_grams
    return result


def transform_lines(recipe: Recipe) -> list[Line]:
    """One serving of the recipe as engine input; needs ``get`` loading."""
    lines = []
    for i in recipe.ingredients:
        food = i.food
        portions = {p.unit: p.grams for p in food.portions}
        lines.append(
            Line(
                key=f"{i.position}:{food.slug}",
                per_100g=to_facts(food).per_100g,
                grams=i.amount_g / recipe.servings,
                role=CulinaryRole(i.culinary_role or food.culinary_roles[0]),
                optional=i.optional,
                piece_g=portions.get(i.display_unit) if i.display_unit else None,
            )
        )
    return lines
