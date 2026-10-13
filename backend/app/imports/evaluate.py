"""Full-recipe import golden set: how well parsing and matching do on whole recipes.

Each recipe is a YAML file (optionally with an HTML page carrying schema.org
Recipe JSON-LD) listing its raw ingredient lines and, per line, the expected
food and grams, or ``slug: null`` when the line must go to a clarification
prompt. The evaluator runs every line through ``parse_line`` + ``match_line``
and measures the Sprint 3 gates (Development Plan §9):

* ingredient match rate: right food, grams within ±5%, no clarification;
* must-ask rate: lines that should ask do ask (no silent guess);
* macro accuracy: per-serving kcal and protein from the lines the import would
  accept without asking, against the expected values, within ±5%.

Expected per-serving macros cover only the lines with an expected food: a
must-ask line is filled in by the user's answer, so it is in neither number.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

import yaml
from sqlalchemy.ext.asyncio import AsyncSession

from app.foods import repository as foods_repo
from app.imports.match import Match, match_line
from app.imports.page import recipe_from_html
from app.imports.parse import parse_line

GRAMS_TOLERANCE = 0.05
MACRO_TOLERANCE = 0.05


class Outcome(StrEnum):
    MATCHED = "matched"  # right food and grams, no question
    ASKED = "asked"  # must-ask line that asks
    FALSE_ASK = "false_ask"  # had a known answer but asked
    WRONG_FOOD = "wrong_food"  # accepted a different food
    WRONG_GRAMS = "wrong_grams"  # right food, grams off by more than 5%
    GUESSED = "guessed"  # must-ask line accepted without asking


@dataclass(frozen=True, slots=True)
class ExpectedLine:
    line: str
    slug: str | None
    grams: float | None = None

    @property
    def must_ask(self) -> bool:
        return self.slug is None


@dataclass(frozen=True, slots=True)
class GoldenRecipe:
    key: str
    title: str
    language: str
    source: str  # blog | caption | cookbook
    servings: int
    kcal: float  # expected per serving
    protein_g: float
    expected: list[ExpectedLine]
    # the lines as the importer sees them: from the YAML, or read from the HTML page
    raw_lines: list[str]
    html: str | None = None


@dataclass(frozen=True, slots=True)
class LineResult:
    expected: ExpectedLine
    raw: str
    match: Match
    outcome: Outcome


@dataclass(frozen=True, slots=True)
class RecipeResult:
    recipe: GoldenRecipe
    lines: list[LineResult]
    kcal: float  # computed per serving
    protein_g: float
    extraction_ok: bool = True  # page lines equal the expected lines

    @property
    def matchable(self) -> int:
        return sum(not r.expected.must_ask for r in self.lines)

    @property
    def matched(self) -> int:
        return sum(r.outcome is Outcome.MATCHED for r in self.lines)

    @property
    def match_rate(self) -> float:
        return self.matched / self.matchable if self.matchable else 1.0

    @property
    def kcal_error(self) -> float:
        return _relative_error(self.kcal, self.recipe.kcal)

    @property
    def protein_error(self) -> float:
        return _relative_error(self.protein_g, self.recipe.protein_g)

    @property
    def kcal_ok(self) -> bool:
        return self.kcal_error <= MACRO_TOLERANCE

    @property
    def protein_ok(self) -> bool:
        return self.protein_error <= MACRO_TOLERANCE


@dataclass
class Report:
    recipes: list[RecipeResult] = field(default_factory=list)

    @property
    def lines(self) -> list[LineResult]:
        return [line for r in self.recipes for line in r.lines]

    def _count(self, *outcomes: Outcome) -> int:
        return sum(line.outcome in outcomes for line in self.lines)

    @property
    def match_rate(self) -> float:
        """Matched lines over lines with an expected food."""
        matchable = sum(r.matchable for r in self.recipes)
        return self._count(Outcome.MATCHED) / matchable if matchable else 1.0

    @property
    def must_ask_rate(self) -> float:
        """Must-ask lines that ask, over all must-ask lines (1.0 when none)."""
        must = self._count(Outcome.ASKED, Outcome.GUESSED)
        return self._count(Outcome.ASKED) / must if must else 1.0

    @property
    def ask_precision(self) -> float:
        """Of the lines that ask, the share that should (the rest are false asks)."""
        asked = self._count(Outcome.ASKED, Outcome.FALSE_ASK)
        return self._count(Outcome.ASKED) / asked if asked else 1.0

    @property
    def kcal_within(self) -> float:
        return _share(r.kcal_ok for r in self.recipes)

    @property
    def protein_within(self) -> float:
        return _share(r.protein_ok for r in self.recipes)

    @property
    def outcomes(self) -> Counter[Outcome]:
        return Counter(line.outcome for line in self.lines)

    @property
    def ask_reasons(self) -> Counter[str]:
        """Why lines with a known answer asked (the false asks)."""
        return Counter(
            line.match.reason or "low confidence"
            for line in self.lines
            if line.outcome is Outcome.FALSE_ASK
        )


def _relative_error(actual: float, expected: float) -> float:
    if expected == 0:
        return 0.0 if actual == 0 else float("inf")
    return abs(actual - expected) / expected


def _share(flags: Iterable[bool]) -> float:
    values = list(flags)
    return sum(values) / len(values) if values else 1.0


# --- loading ---------------------------------------------------------------


def load_recipe(path: Path) -> GoldenRecipe:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    expected = [ExpectedLine(c["line"], c["slug"], c.get("grams")) for c in data["lines"]]
    raw_lines = [e.line for e in expected]
    html = data.get("html")
    if html:
        page = recipe_from_html(
            (path.parent / html).read_text(encoding="utf-8"), f"https://example.com/{path.stem}"
        )
        raw_lines = page.ingredients if page else []
    macros = data["expected_per_serving"]
    return GoldenRecipe(
        key=path.stem,
        title=data["title"],
        language=data["language"],
        source=data["source"],
        servings=int(data["servings"]),
        kcal=float(macros["kcal"]),
        protein_g=float(macros["protein_g"]),
        expected=expected,
        raw_lines=raw_lines,
        html=html,
    )


def load_recipes(directory: Path) -> list[GoldenRecipe]:
    return [load_recipe(p) for p in sorted(directory.glob("*.yaml"))]


# --- evaluation ------------------------------------------------------------


def _outcome(expected: ExpectedLine, match: Match) -> Outcome:
    if expected.must_ask:
        return Outcome.ASKED if match.needs_clarification else Outcome.GUESSED
    if match.needs_clarification:
        return Outcome.FALSE_ASK
    if match.slug != expected.slug:
        return Outcome.WRONG_FOOD
    assert match.grams is not None and expected.grams is not None
    if abs(match.grams - expected.grams) > GRAMS_TOLERANCE * expected.grams:
        return Outcome.WRONG_GRAMS
    return Outcome.MATCHED


async def _per_serving(
    session: AsyncSession, items: list[tuple[str, float]], servings: int
) -> tuple[float, float]:
    """(kcal, protein_g) per serving for (slug, grams) pairs."""
    foods = await foods_repo.get_by_slugs(session, sorted({slug for slug, _ in items}))
    kcal = protein = 0.0
    for slug, grams in items:
        food = foods[slug]
        kcal += food.kcal * grams / 100
        protein += food.protein_g * grams / 100
    return kcal / servings, protein / servings


async def expected_per_serving(session: AsyncSession, recipe: GoldenRecipe) -> tuple[float, float]:
    """The recipe's per-serving (kcal, protein_g) from its expected foods and grams."""
    items = [(e.slug, e.grams) for e in recipe.expected if e.slug and e.grams is not None]
    return await _per_serving(session, items, recipe.servings)


async def evaluate_recipe(session: AsyncSession, recipe: GoldenRecipe) -> RecipeResult:
    extraction_ok = recipe.raw_lines == [e.line for e in recipe.expected]
    results = []
    for i, expected in enumerate(recipe.expected):
        raw = recipe.raw_lines[i] if i < len(recipe.raw_lines) else ""
        match = await match_line(session, parse_line(raw))
        results.append(LineResult(expected, raw, match, _outcome(expected, match)))
    accepted = [
        (r.match.slug, r.match.grams)
        for r in results
        if not r.match.needs_clarification and r.match.slug and r.match.grams is not None
    ]
    kcal, protein = await _per_serving(session, accepted, recipe.servings)
    return RecipeResult(recipe, results, kcal, protein, extraction_ok)


async def evaluate(session: AsyncSession, recipes: list[GoldenRecipe]) -> Report:
    """Needs the foods loaded; see ``tests/test_import_eval.py``."""
    return Report([await evaluate_recipe(session, r) for r in recipes])


# --- report ----------------------------------------------------------------


def _describe(line: LineResult) -> str:
    m = line.match
    e = line.expected
    want = "ask" if e.must_ask else f"{e.slug} {e.grams:g} g"
    got = f"{m.slug} {m.grams:.4g} g" if m.grams is not None else f"{m.slug} ? g"
    if m.needs_clarification:
        got = f"ask ({m.reason or 'low confidence'}; best {got}, conf {m.confidence:g})"
    return f"{line.outcome.value}: {line.raw!r}: want {want}, got {got}"


def render(report: Report, *, details: bool = True) -> str:
    out = [
        f"recipes: {len(report.recipes)}, lines: {len(report.lines)}",
        f"ingredient match rate: {report.match_rate:.1%}",
        f"must-ask lines that ask: {report.must_ask_rate:.1%}",
        f"clarification precision (asks that should ask): {report.ask_precision:.1%}",
        f"recipes within ±5% kcal: {report.kcal_within:.1%}",
        f"recipes within ±5% protein: {report.protein_within:.1%}",
        "outcomes: " + ", ".join(f"{o.value} {n}" for o, n in report.outcomes.most_common()),
    ]
    for language in sorted({r.recipe.language for r in report.recipes}):
        part = Report([r for r in report.recipes if r.recipe.language == language])
        out.append(
            f"  {language}: match {part.match_rate:.1%}, must-ask {part.must_ask_rate:.1%}, "
            f"kcal within ±5% {part.kcal_within:.1%} ({len(part.recipes)} recipes)"
        )
    if report.ask_reasons:
        out.append(
            "false-ask reasons: "
            + ", ".join(f"{reason} {n}" for reason, n in report.ask_reasons.most_common())
        )
    for r in report.recipes:
        signed = r.kcal / r.recipe.kcal - 1 if r.recipe.kcal else 0.0
        flag = "" if r.extraction_ok else " [page lines differ from expected]"
        out.append(
            f"{r.recipe.key}: {r.matched}/{r.matchable} matched, "
            f"kcal {r.kcal:.0f} vs {r.recipe.kcal:.0f} ({signed:+.1%}), "
            f"protein {r.protein_g:.1f} vs {r.recipe.protein_g:.1f}{flag}"
        )
        if details:
            out.extend(
                f"  - {_describe(line)}"
                for line in r.lines
                if line.outcome not in (Outcome.MATCHED, Outcome.ASKED)
            )
    return "\n".join(out)
