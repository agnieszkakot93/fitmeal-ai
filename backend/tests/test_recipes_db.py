import pytest
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.foods import importer
from app.foods.curated import load_curated
from app.foods.fdc import load_fdc_dirs
from app.foods.models import FoodItem
from app.foods.repository import get_by_slugs
from app.recipes import repository
from app.recipes.models import (
    Recipe,
    RecipeIngredient,
    RecipeSource,
    RecipeVariant,
    SourceType,
)
from tests.test_foods_db import CURATED, FDC_FIXTURES


@pytest.fixture
async def foods(db_session: AsyncSession) -> AsyncSession:
    report = importer.resolve(load_curated(CURATED), load_fdc_dirs([FDC_FIXTURES]))
    await importer.apply(db_session, report.resolved)
    await db_session.commit()
    return db_session


async def _recipe(session: AsyncSession) -> Recipe:
    found = await get_by_slugs(session, ["chicken-breast-raw", "rice-white-dry", "olive-oil"])
    recipe = Recipe(
        slug="chicken-rice-bowl",
        title_en="Chicken rice bowl",
        servings=2,
        source=RecipeSource(type=SourceType.CATALOG, public_usage_status="public"),
        ingredients=[
            RecipeIngredient(position=0, food=found["chicken-breast-raw"], amount_g=300),
            RecipeIngredient(position=1, food=found["rice-white-dry"], amount_g=150),
            RecipeIngredient(
                position=2,
                food=found["olive-oil"],
                amount_g=13.5,
                display_amount=1,
                display_unit="tbsp",
            ),
        ],
    )
    session.add(recipe)
    await session.commit()
    return recipe


async def test_refresh_nutrition_caches_totals_from_ingredients(foods: AsyncSession) -> None:
    created = await _recipe(foods)
    recipe = await repository.get(foods, created.id)
    assert recipe is not None
    result = repository.refresh_nutrition(recipe)
    await foods.commit()

    assert recipe.total_grams == pytest.approx(463.5)
    assert recipe.kcal == pytest.approx(result.total.kcal)
    assert result.per_serving.kcal == pytest.approx(result.total.kcal / 2)
    assert [i.position for i in recipe.ingredients] == [0, 1, 2]


async def test_variants_keep_lineage_and_cascade_with_the_recipe(foods: AsyncSession) -> None:
    recipe = await _recipe(foods)
    shared = RecipeVariant(base_recipe=recipe, label="high-protein", targets={"protein_g": 45})
    foods.add(shared)
    await foods.flush()
    foods.add(RecipeVariant(base_recipe=recipe, parent_variant_id=shared.id))
    await foods.commit()

    await foods.delete(recipe)
    await foods.commit()
    assert (await repository.get(foods, recipe.id)) is None


async def test_imported_source_cannot_be_public(foods: AsyncSession) -> None:
    foods.add(
        RecipeSource(type=SourceType.LINK, reference="https://x", public_usage_status="public")
    )
    with pytest.raises(IntegrityError, match="imports_private"):
        await foods.commit()


async def test_food_in_a_recipe_cannot_be_deleted(foods: AsyncSession) -> None:
    await _recipe(foods)
    with pytest.raises(IntegrityError, match="fk_recipe_ingredients_food_id"):
        await foods.execute(delete(FoodItem).where(FoodItem.slug == "olive-oil"))
