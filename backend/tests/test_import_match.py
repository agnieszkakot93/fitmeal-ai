"""Ingredient matching against the real curated foods (committed FDC snapshot).

The golden set is the Sprint 3 gate for ingredient matching: at least 90% of
lines must match the expected food without a clarification prompt
(Development Plan §9), and lines marked ``slug: null`` must ask instead of guess.
"""

from pathlib import Path

import pytest
import yaml
from sqlalchemy.ext.asyncio import AsyncSession

from app.foods import importer
from app.foods.curated import load_curated
from app.foods.fdc import load_fdc_dirs
from app.imports.match import match_line
from app.imports.parse import parse_line
from tests.test_foods_db import CURATED, ROOT

GOLDEN = Path(__file__).parent / "fixtures" / "import_golden.yaml"
SNAPSHOT = ROOT / "data" / "foods" / "fdc_snapshot"
MATCH_RATE_GATE = 0.9


@pytest.fixture
async def foods(db_session: AsyncSession) -> AsyncSession:
    report = importer.resolve(load_curated(CURATED), load_fdc_dirs([SNAPSHOT]))
    await importer.apply(db_session, report.resolved)
    await db_session.commit()
    return db_session


async def test_golden_set(foods: AsyncSession) -> None:
    cases = yaml.safe_load(GOLDEN.read_text(encoding="utf-8"))["lines"]
    expected_matches = [c for c in cases if c["slug"]]
    failures = []
    hits = 0
    for case in cases:
        match = await match_line(foods, parse_line(case["line"]))
        if case["slug"] is None:
            if not match.needs_clarification:
                failures.append(f"guessed {match.slug} for {case['line']!r}")
            continue
        ok = (
            match.slug == case["slug"]
            and not match.needs_clarification
            and match.grams == pytest.approx(case["grams"], rel=0.05)
        )
        hits += ok
        if not ok:
            failures.append(
                f"{case['line']!r}: got {match.slug} {match.grams} "
                f"conf={match.confidence} ({match.reason}); top={match.candidates[:3]}"
            )
    rate = hits / len(expected_matches)
    assert rate >= MATCH_RATE_GATE and not [f for f in failures if "guessed" in f], (
        f"match rate {rate:.0%}\n" + "\n".join(failures)
    )
