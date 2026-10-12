"""Transformation hit rates on the real catalog and the committed FDC snapshot.

Guards against regressions in role bounds, rounding and weights. The floors
are the rates measured when the engine was tuned (2026-10-12, with same-group
substitutions): raise them when
the engine improves, never lower them to make a change pass.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.foods import importer
from app.foods.curated import load_curated
from app.foods.fdc import load_fdc_dirs
from app.recipes import catalog, tuning
from tests.test_foods_db import CURATED, ROOT

SNAPSHOT = ROOT / "data" / "foods" / "fdc_snapshot"
CATALOG = ROOT / "data" / "recipes" / "catalog.yaml"

FLOORS = {
    "cut 20% kcal, keep protein": 52,
    "add 20% kcal, keep protein": 60,
    "25% more protein, same kcal": 51,
}


async def test_catalog_hit_rates_do_not_regress(db_session: AsyncSession) -> None:
    report = importer.resolve(load_curated(CURATED), load_fdc_dirs([SNAPSHOT]))
    assert not report.unmatched
    await importer.apply(db_session, report.resolved)
    written = await catalog.apply(db_session, catalog.load_catalog(CATALOG))
    await db_session.commit()
    assert len(written.written) == 60

    results = await tuning.evaluate(db_session)
    hits = {name: r.hits for name, r in results.items()}
    for name, floor in FLOORS.items():
        assert hits[name] >= floor, tuning.render(results)
