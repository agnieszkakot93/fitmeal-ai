"""A draft's lines matched to foods, with the questions the user must answer (PRD §8.1)."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.foods import repository as foods_repo
from app.foods.models import FoodItem
from app.importjobs.extract import Draft
from app.importjobs.schemas import (
    Candidate,
    Clarification,
    ClarificationKind,
    PreviewLine,
    PreviewOut,
)
from app.imports.match import Match, match_line
from app.imports.parse import parse_line


def _candidate(foods: dict[str, FoodItem], slug: str, score: float) -> Candidate | None:
    food = foods.get(slug)
    if food is None:
        return None
    return Candidate(slug=slug, name_en=food.name_en, name_pl=food.name_pl, score=score)


def _line(position: int, m: Match, foods: dict[str, FoodItem]) -> PreviewLine:
    candidates = [c for slug, s in m.candidates if (c := _candidate(foods, slug, s))]
    return PreviewLine(
        position=position,
        raw=m.line.raw,
        amount=m.line.amount,
        unit=m.line.unit,
        name=m.line.name,
        note=m.line.note,
        optional=m.line.optional,
        weight_g=m.line.weight_g,
        food=_candidate(foods, m.slug, m.confidence) if m.slug else None,
        grams=round(m.grams, 1) if m.grams is not None else None,
        confidence=m.confidence,
        needs_clarification=m.needs_clarification,
        candidates=candidates,
    )


async def build(session: AsyncSession, draft: Draft, source_url: str | None) -> PreviewOut:
    matches = [await match_line(session, parse_line(raw)) for raw in draft.ingredients]
    slugs = {m.slug for m in matches if m.slug} | {s for m in matches for s, _ in m.candidates}
    foods = await foods_repo.get_by_slugs(session, sorted(slugs))
    lines = [_line(i, m, foods) for i, m in enumerate(matches)]
    questions = [
        Clarification(
            kind=ClarificationKind.INGREDIENT,
            position=line.position,
            question=m.reason or "which ingredient?",
            candidates=line.candidates,
        )
        for line, m in zip(lines, matches, strict=True)
        if line.needs_clarification
    ]
    if draft.servings is None:
        questions.append(
            Clarification(kind=ClarificationKind.SERVINGS, position=None, question="how many?")
        )
    if not draft.title:
        questions.append(
            Clarification(kind=ClarificationKind.TITLE, position=None, question="what is it?")
        )
    return PreviewOut(
        title=draft.title,
        servings=draft.servings,
        language=draft.language,
        source_url=source_url,
        instructions=draft.instructions,
        ingredients=lines,
        clarifications=questions,
        confidence=min((line.confidence for line in lines), default=0.0),
    )
