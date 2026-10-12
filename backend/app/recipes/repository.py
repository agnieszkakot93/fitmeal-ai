from __future__ import annotations

import uuid
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.foods import repository as foods_repo
from app.foods.models import FoodItem
from app.foods.repository import to_allergens, to_facts
from app.foods.vocab import CulinaryRole
from app.nutrition.allergens import Allergen, Exclusion, IngredientAllergens, Origin, TraceStatus
from app.nutrition.calc import IngredientLine, RecipeNutrition, calculate
from app.optimizer.substitute import Option, options
from app.optimizer.transform import Line
from app.recipes.models import Recipe, RecipeIngredient
from app.recipes.safety import CheckLine, RecipeAllergens, RecipeCheck, check, combine


async def get(session: AsyncSession, recipe_id: uuid.UUID) -> Recipe | None:
    """A recipe with its ingredients and their foods (with portions and aliases) loaded."""
    stmt = (
        select(Recipe)
        .where(Recipe.id == recipe_id)
        .options(
            selectinload(Recipe.ingredients)
            .selectinload(RecipeIngredient.food)
            .options(selectinload(FoodItem.portions), selectinload(FoodItem.aliases))
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


def _effective(food: FoodItem) -> IngredientAllergens:
    """Allergen facts without names; enough for ``combine``, no aliases needed."""
    return IngredientAllergens(
        origin=Origin(food.origin),
        contains=frozenset(Allergen(a) for a in food.effective_allergens),
        may_contain=frozenset(Allergen(a) for a in food.effective_may_contain),
        trace_status=TraceStatus(food.effective_trace_status),
    )


def refresh_allergens(recipe: Recipe) -> RecipeAllergens:
    """Recompute and store the cached allergens. Call after any ingredient change."""
    result = combine(_effective(i.food) for i in recipe.ingredients)
    recipe.allergens = sorted(result.contains)
    recipe.may_contain = sorted(result.may_contain)
    recipe.trace_status = result.trace_status.value
    return result


def check_exclusions(recipe: Recipe, exclusions: list[Exclusion]) -> RecipeCheck:
    """Per-ingredient conflicts with the user's exclusions; needs ``get`` loading."""
    lines = [
        CheckLine(f"{i.position}:{i.food.slug}", to_allergens(i.food), i.optional)
        for i in recipe.ingredients
    ]
    return check(lines, exclusions)


@dataclass(frozen=True, slots=True)
class Fix:
    """What to do about one excluded ingredient (PRD §8.3 steps 1-2)."""

    key: str
    remove: bool  # an optional ingredient: just leave it out
    substitutes: list[Option]  # ranked; empty means no safe substitute was found


async def propose_fixes(
    session: AsyncSession, recipe: Recipe, exclusions: list[Exclusion]
) -> list[Fix]:
    """Fixes for every excluded ingredient; nothing changes until the user picks one."""
    result = check_exclusions(recipe, exclusions)
    fixes = []
    for ingredient in recipe.ingredients:
        key = f"{ingredient.position}:{ingredient.food.slug}"
        if key in result.must_remove:
            fixes.append(Fix(key, remove=True, substitutes=[]))
        elif key in result.must_substitute:
            food = ingredient.food
            role = ingredient.culinary_role or food.culinary_roles[0]
            candidates = await foods_repo.substitution_candidates(session, food, role)
            ranked = options(
                foods_repo.to_substitution_food(food),
                ingredient.amount_g / recipe.servings,
                CulinaryRole(role),
                [foods_repo.to_substitution_food(c) for c in candidates],
                exclusions,
            )
            fixes.append(Fix(key, remove=False, substitutes=ranked))
    return fixes


# roles where swapping the food is a normal cook's move
SWAPPABLE_ROLES = {
    CulinaryRole.MAIN_PROTEIN,
    CulinaryRole.CARB_BASE,
    CulinaryRole.CREAMY_BASE,
    CulinaryRole.CHEESE,
    CulinaryRole.COOKING_FAT,
    CulinaryRole.LIQUID,
}


async def substitution_alternatives(
    session: AsyncSession,
    recipe: Recipe,
    exclusions: list[Exclusion] | None = None,
    per_line: int = 3,
) -> dict[str, list[Line]]:
    """Top safe, not-disliked, same-group substitutes per swappable line, as engine lines.

    Only close swaps (same substitution group: chicken -> turkey, rice -> buckwheat)
    are proposed automatically; wider ones (chicken -> tofu) stay a user choice
    through the Swap screen. Keys match :func:`transform_lines`; amounts are per
    serving. Needs ``get`` loading.
    """
    result: dict[str, list[Line]] = {}
    for line, ingredient in zip(transform_lines(recipe), recipe.ingredients, strict=True):
        if line.role not in SWAPPABLE_ROLES:
            continue
        food = ingredient.food
        candidates = await foods_repo.substitution_candidates(session, food, line.role.value)
        by_slug = {c.slug: c for c in candidates}
        ranked = options(
            foods_repo.to_substitution_food(food),
            line.grams,
            line.role,
            [foods_repo.to_substitution_food(c) for c in candidates],
            exclusions or [],
            limit=per_line * 2,
        )
        alts = [
            Line(
                key=f"{line.key}=>{o.key}",
                per_100g=to_facts(by_slug[o.key]).per_100g,
                grams=o.grams,
                role=line.role,
                optional=line.optional,
            )
            for o in ranked
            if o.same_group and not o.disliked
        ]
        if alts:
            result[line.key] = alts[:per_line]
    return result
