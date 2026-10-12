import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.foods import importer
from app.foods.curated import load_curated
from app.foods.fdc import load_fdc_dirs
from app.recipes import catalog
from app.recipes.models import Recipe, RecipeIngredient
from tests.test_foods_db import CURATED, FDC_FIXTURES, ROOT

CATALOG = ROOT / "data" / "recipes" / "catalog.yaml"


def _entry(slug: str, ingredients: list[dict[str, object]]) -> dict[str, object]:
    return {
        "slug": slug,
        "title": {"en": "Test", "pl": "Test"},
        "servings": 2,
        "prep_minutes": 5,
        "cook_minutes": 10,
        "difficulty": "easy",
        "storage": {"fridge_days": 2},
        "meal_prep_score": 50,
        "ingredients": ingredients,
        "steps": {"en": ["Cook."], "pl": ["Ugotuj."]},
    }


def test_catalog_has_60_recipes_that_resolve_against_the_food_list() -> None:
    recipes = catalog.load_catalog(CATALOG)
    assert len(recipes.recipes) == 60
    assert catalog.check_against_foods(recipes, load_curated(CURATED)) == []


def test_steps_must_match_in_both_languages() -> None:
    entry = _entry("x", [{"food": "olive-oil", "amount": 1}])
    entry["steps"] = {"en": ["One.", "Two."], "pl": ["Jeden."]}
    with pytest.raises(ValueError, match="same number of steps"):
        catalog.CatalogFile.model_validate({"recipes": [entry]})


def test_unknown_and_unconvertible_foods_are_reported() -> None:
    recipes = catalog.CatalogFile.model_validate(
        {
            "recipes": [
                _entry(
                    "x",
                    [
                        {"food": "no-such-food", "amount": 1},
                        {"food": "chicken-breast-raw", "amount": 1, "unit": "tbsp"},
                        {"food": "skyr-natural", "amount": 100},
                    ],
                )
            ]
        }
    )
    problems = catalog.check_against_foods(recipes, load_curated(CURATED))
    assert len(problems) == 3


@pytest.fixture
async def foods(db_session: AsyncSession) -> AsyncSession:
    report = importer.resolve(load_curated(CURATED), load_fdc_dirs([FDC_FIXTURES]))
    await importer.apply(db_session, report.resolved)
    await db_session.commit()
    return db_session


async def test_apply_converts_units_and_is_idempotent(foods: AsyncSession) -> None:
    recipes = catalog.CatalogFile.model_validate(
        {
            "recipes": [
                _entry(
                    "egg-rice",
                    [
                        {"food": "rice-white-dry", "amount": 100},
                        {"food": "egg-whole-raw", "amount": 2, "unit": "piece"},
                        {"food": "olive-oil", "amount": 1, "unit": "tbsp"},
                    ],
                ),
                _entry("needs-salmon", [{"food": "salmon-atlantic-raw", "amount": 100}]),
            ]
        }
    )
    report = await catalog.apply(foods, recipes)
    await foods.commit()
    assert report.written == ["egg-rice"]
    assert report.skipped == {"needs-salmon": ["salmon-atlantic-raw"]}

    again = await catalog.apply(foods, recipes)
    await foods.commit()
    assert again.written == ["egg-rice"]
    assert await foods.scalar(select(func.count()).select_from(Recipe)) == 1

    rows = (await foods.scalars(select(RecipeIngredient).order_by(RecipeIngredient.position))).all()
    assert [r.amount_g for r in rows] == pytest.approx([100, 100, 15 * 0.91])
    assert (rows[1].display_amount, rows[1].display_unit) == (2, "piece")
    assert rows[0].display_unit is None
    recipe = await foods.scalar(select(Recipe))
    assert recipe is not None and recipe.kcal is not None and recipe.kcal > 0
    assert recipe.source_id is not None
