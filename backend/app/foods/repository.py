from __future__ import annotations

from sqlalchemy import case, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.text import fold
from app.foods.models import FoodAlias, FoodItem
from app.nutrition.calc import FoodFacts
from app.nutrition.nutrients import Nutrients
from app.nutrition.units import FoodUnitData

_WITH_CHILDREN = (
    selectinload(FoodItem.aliases),
    selectinload(FoodItem.portions),
    selectinload(FoodItem.packages),
)


async def get_by_slug(session: AsyncSession, slug: str) -> FoodItem | None:
    result = await session.scalars(
        select(FoodItem).where(FoodItem.slug == slug).options(*_WITH_CHILDREN)
    )
    return result.first()


async def get_by_slugs(session: AsyncSession, slugs: list[str]) -> dict[str, FoodItem]:
    result = await session.scalars(
        select(FoodItem).where(FoodItem.slug.in_(slugs)).options(*_WITH_CHILDREN)
    )
    return {item.slug: item for item in result}


async def search(
    session: AsyncSession, query: str, lang: str | None = None, limit: int = 20
) -> list[tuple[FoodItem, float]]:
    """Best alias match per food, ranked by trigram similarity (prefix hits first)."""
    q = fold(query)
    if not q:
        return []
    score = func.greatest(
        func.similarity(FoodAlias.alias_folded, q),
        # "kurcz" should find "kurczak" even when the trigram score is low
        case((FoodAlias.alias_folded.startswith(q), 0.9), else_=0.0),
    )
    best = (
        select(FoodAlias.food_id, func.max(score).label("score"))
        .where(or_(FoodAlias.alias_folded.op("%")(q), FoodAlias.alias_folded.contains(q)))
        .group_by(FoodAlias.food_id)
    )
    if lang is not None:
        best = best.where(FoodAlias.lang == lang)
    sub = best.subquery()
    rows = await session.execute(
        select(FoodItem, sub.c.score)
        .join(sub, sub.c.food_id == FoodItem.id)
        .order_by(sub.c.score.desc(), FoodItem.slug)
        .limit(limit)
    )
    return [(item, float(s)) for item, s in rows.all()]


def to_facts(item: FoodItem) -> FoodFacts:
    return FoodFacts(
        key=item.slug,
        per_100g=Nutrients(item.kcal, item.protein_g, item.fat_g, item.carbs_g, item.fiber_g),
        units=FoodUnitData(
            density_g_per_ml=item.density_g_per_ml,
            portions_g={p.unit: p.grams for p in item.portions},
        ),
    )
