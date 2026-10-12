import pytest
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.foods import importer
from app.foods.curated import load_curated
from app.foods.fdc import load_fdc_dirs
from app.foods.models import FoodItem
from app.foods.repository import get_by_slugs
from app.nutrition.allergens import Exclusion, ExclusionCategory, Severity
from app.optimizer.transform import Target, transform
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


async def test_stored_recipe_transforms_per_serving(foods: AsyncSession) -> None:
    created = await _recipe(foods)
    recipe = await repository.get(foods, created.id)
    assert recipe is not None
    lines = repository.transform_lines(recipe)
    assert [ln.grams for ln in lines] == pytest.approx([150, 75, 6.75])
    assert lines[2].piece_g is None  # tbsp is a volume unit, not a portion

    per_serving = repository.compute_nutrition(recipe).per_serving
    result = transform(lines, Target(per_serving.kcal * 0.85, per_serving.protein_g))
    assert result.on_target, result.misses


async def test_allergens_are_cached_and_fixes_proposed(foods: AsyncSession) -> None:
    found = await get_by_slugs(foods, ["egg-whole-raw", "rice-white-dry", "milk-skim"])
    recipe = Recipe(
        slug="egg-rice",
        title_en="Egg rice",
        servings=1,
        source=RecipeSource(type=SourceType.CATALOG, public_usage_status="public"),
        ingredients=[
            RecipeIngredient(
                position=0, food=found["egg-whole-raw"], amount_g=100, culinary_role="main_protein"
            ),
            RecipeIngredient(position=1, food=found["rice-white-dry"], amount_g=80),
            RecipeIngredient(position=2, food=found["milk-skim"], amount_g=50, optional=True),
        ],
    )
    foods.add(recipe)
    await foods.flush()
    loaded = await repository.get(foods, recipe.id)
    assert loaded is not None
    repository.refresh_allergens(loaded)
    await foods.commit()
    assert set(loaded.allergens) == {"eggs", "milk"}

    exclusions = [
        Exclusion(ExclusionCategory.EGGS, Severity.ALLERGY),
        Exclusion(ExclusionCategory.DAIRY, Severity.ALLERGY),
    ]
    assert repository.check_exclusions(loaded, exclusions).blocked
    fixes = {f.key: f for f in await repository.propose_fixes(foods, loaded, exclusions)}
    assert fixes["2:milk-skim"].remove
    egg = fixes["0:egg-whole-raw"]
    assert not egg.remove
    assert [o.key for o in egg.substitutes] == ["chicken-breast-raw"]
