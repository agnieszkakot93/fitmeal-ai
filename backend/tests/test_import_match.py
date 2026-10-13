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


@pytest.mark.parametrize(
    ("line", "slug", "grams"),
    [
        # Polish cases and adjective endings match whole words, not trigrams
        ("2 łyżki oliwy", "olive-oil", 27.3),
        ("500 g mąki pszennej", "flour-wheat", 500),
        ("1 łyżka mąki", "flour-wheat", 8),  # not "mak" (poppy seed)
        ("2 łyżki cukru", "sugar-white", 25),
        ("10 czarnych oliwek", "olives-black", 40),
        ("1 łyżka masła", "butter", 14),  # not "maślanka" (buttermilk)
        # descriptor words don't make a line unknown
        ("250 ml ciepłego mleka", "milk-2", 257.5),
        ("100g mrożonych truskawek", "strawberries", 100),
        ("100 g shredded lettuce", "romaine-lettuce", 100),
        # the more specific alias wins a tie
        ("1 łyżeczka imbiru mielonego", "ginger-ground", 1.8),
        ("1 łyżeczka papryki słodkiej", "paprika-sweet", 2.3),
        # units after the name, in a note, or as the only amount
        ("2 garlic cloves", "garlic", 8),
        ("2 cukinie (ok. 600 g)", "zucchini", 600),
        ("a handful of baby spinach", "spinach", 30),
        # a can picks the canned food
        ("1 puszka pomidorów", "tomatoes-canned", 400),
        ("1 can (28 oz) crushed tomatoes", "tomatoes-canned", 793.8),
    ],
)
async def test_matches_without_asking(
    foods: AsyncSession, line: str, slug: str, grams: float
) -> None:
    match = await match_line(foods, parse_line(line))
    assert (match.slug, match.needs_clarification) == (slug, False), match
    assert match.grams == pytest.approx(grams, rel=0.05)


@pytest.mark.parametrize(
    "line",
    [
        "sól, pieprz",
        "6 cups vegetable broth",  # not "vegetable oil"
        "1 tbsp sesame oil",  # not sesame seeds
        "1/2 cup oat flour",  # not wheat flour
        "1 cup rice flour",
    ],
)
async def test_asks_instead_of_a_wrong_food(foods: AsyncSession, line: str) -> None:
    match = await match_line(foods, parse_line(line))
    assert match.needs_clarification, match
