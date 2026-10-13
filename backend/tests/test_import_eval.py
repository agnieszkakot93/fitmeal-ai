"""Full-recipe import golden set against the real curated foods (committed FDC snapshot).

The Sprint 3 go/no-go gates (Development Plan §9): at least 90% of ingredient
lines match the right food and grams without a clarification prompt, every
must-ask line asks, and at least 90% of recipes land within ±5% of the
expected per-serving kcal. A gate the matcher misses is marked
``xfail(strict=True)`` until it reaches it. The floors below are the measured
rates: raise them when the matcher improves, never lower them.
"""

from pathlib import Path

import pytest
import yaml
from sqlalchemy.ext.asyncio import AsyncSession

from app.foods import importer
from app.foods.curated import load_curated
from app.foods.fdc import load_fdc_dirs
from app.imports import evaluate
from app.imports.page import recipe_from_html
from tests.test_foods_db import CURATED, ROOT

RECIPES = Path(__file__).parent / "fixtures" / "import_recipes"
SNAPSHOT = ROOT / "data" / "foods" / "fdc_snapshot"

MATCH_RATE_GATE = 0.9
KCAL_WITHIN_GATE = 0.9
# measured 2026-10-13 when the set was added: match 84.3%, must-ask 87.3%, kcal 42.6%;
# after whole-word (inflection-aware) matching: 100% on all three
FLOORS = {"match_rate": 1.0, "must_ask_rate": 1.0, "kcal_within": 1.0}


@pytest.fixture
async def report(db_session: AsyncSession) -> evaluate.Report:
    resolved = importer.resolve(load_curated(CURATED), load_fdc_dirs([SNAPSHOT]))
    await importer.apply(db_session, resolved.resolved)
    await db_session.commit()
    return await evaluate.evaluate(db_session, evaluate.load_recipes(RECIPES))


def test_set_shape() -> None:
    recipes = evaluate.load_recipes(RECIPES)
    assert 45 <= len(recipes) <= 60
    languages = [r.language for r in recipes]
    assert set(languages) == {"pl", "en"}
    assert abs(languages.count("pl") - languages.count("en")) <= len(recipes) * 0.2
    assert {r.source for r in recipes} == {"blog", "caption", "cookbook"}
    assert 5 <= sum(r.html is not None for r in recipes) <= 8
    for r in recipes:
        assert r.servings > 0 and r.kcal > 0, r.key
        for e in r.expected:
            assert (e.grams is None) == e.must_ask, (r.key, e.line)


def test_expected_foods_exist_with_nutrition() -> None:
    """Expected slugs must be curated foods that the importer resolves."""
    resolved = importer.resolve(load_curated(CURATED), load_fdc_dirs([SNAPSHOT]))
    known = {f.curated.slug for f in resolved.resolved}
    missing = {
        (r.key, e.slug)
        for r in evaluate.load_recipes(RECIPES)
        for e in r.expected
        if e.slug and e.slug not in known
    }
    assert not missing


def test_html_pages_yield_the_expected_lines() -> None:
    for path in sorted(RECIPES.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not data.get("html"):
            continue
        page = recipe_from_html((RECIPES / data["html"]).read_text(encoding="utf-8"), "https://x")
        assert page is not None, path.name
        assert page.name == data["title"]
        assert page.ingredients == [c["line"] for c in data["lines"]]
        assert page.servings == str(data["servings"])
        assert page.language == data["language"]
        assert page.instructions


async def test_expected_macros_match_expected_lines(db_session: AsyncSession) -> None:
    """The stored per-serving numbers follow from the expected foods and grams."""
    resolved = importer.resolve(load_curated(CURATED), load_fdc_dirs([SNAPSHOT]))
    await importer.apply(db_session, resolved.resolved)
    await db_session.commit()
    wrong = []
    for r in evaluate.load_recipes(RECIPES):
        kcal, protein = await evaluate.expected_per_serving(db_session, r)
        if abs(kcal - r.kcal) > 1 or abs(protein - r.protein_g) > 0.15:
            wrong.append(f"{r.key}: kcal {kcal:.0f}, protein_g {protein:.1f}")
    assert not wrong


async def test_rates_do_not_regress(report: evaluate.Report) -> None:
    rendered = evaluate.render(report)
    assert all(r.extraction_ok for r in report.recipes), rendered
    for name, floor in FLOORS.items():
        assert getattr(report, name) >= floor, rendered


async def test_gate_match_rate(report: evaluate.Report) -> None:
    assert report.match_rate >= MATCH_RATE_GATE, evaluate.render(report)


async def test_gate_must_ask_lines_ask(report: evaluate.Report) -> None:
    assert report.must_ask_rate == 1.0, evaluate.render(report)


async def test_gate_kcal_within_5_percent(report: evaluate.Report) -> None:
    assert report.kcal_within >= KCAL_WITHIN_GATE, evaluate.render(report)
