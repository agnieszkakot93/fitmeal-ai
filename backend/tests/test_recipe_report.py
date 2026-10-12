from sqlalchemy.ext.asyncio import AsyncSession

from app.foods import importer
from app.foods.curated import load_curated
from app.foods.fdc import load_fdc_dirs
from app.nutrition.nutrients import Nutrients
from app.recipes import catalog, report
from tests.test_foods_db import CURATED, FDC_FIXTURES
from tests.test_recipe_catalog import _entry


def test_flags() -> None:
    meal = ["lunch", "high_protein"]
    assert report.flags_for(meal, Nutrients(500, 40, 15, 50, 5), 400) == []
    flags = report.flags_for(meal, Nutrients(150, 8, 12, 2, 0), 900)
    assert flags == [
        "low kcal for a meal",
        "fat over 45% of kcal",
        "tagged high_protein but under 25 g",
        "under 10 g protein",
        "portion over 800 g",
    ]
    assert report.flags_for(["snack"], Nutrients(150, 5, 2, 25, 1), 100) == []
    snack = ["snack", "high_protein"]
    assert report.flags_for(snack, Nutrients(200, 17, 2, 25, 1), 250) == []
    assert report.flags_for(snack, Nutrients(200, 12, 2, 25, 1), 250) == [
        "tagged high_protein but under 15 g"
    ]
    assert report.flags_for(["lunch", "soup"], Nutrients(400, 39, 7, 39, 0), 960) == []


async def test_build_and_render(db_session: AsyncSession) -> None:
    resolved = importer.resolve(load_curated(CURATED), load_fdc_dirs([FDC_FIXTURES])).resolved
    await importer.apply(db_session, resolved)
    lines = [
        {"food": "rice-white-dry", "amount": 100},
        {"food": "egg-whole-raw", "amount": 2, "unit": "piece"},
    ]
    entry = _entry("egg-rice", lines)
    await catalog.apply(db_session, catalog.CatalogFile.model_validate({"recipes": [entry]}))
    await db_session.commit()

    rows = await report.build(db_session)
    assert [r.slug for r in rows] == ["egg-rice"]
    assert rows[0].grams_per_serving == 100
    assert "1 recipes, " in report.render(rows)
