from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.foods import repository
from app.foods.schemas import FoodDetail, FoodSearchHit, FoodSummary

router = APIRouter(prefix="/v1/foods", tags=["foods"])

Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("/search", response_model=list[FoodSearchHit])
async def search_foods(
    session: Session,
    q: Annotated[str, Query(min_length=1, max_length=100)],
    lang: Literal["en", "pl"] | None = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
) -> list[FoodSearchHit]:
    hits = await repository.search(session, q, lang=lang, limit=limit)
    return [
        FoodSearchHit(**FoodSummary.of(item).model_dump(), score=round(score, 3))
        for item, score in hits
    ]


@router.get("/{slug}", response_model=FoodDetail)
async def get_food(session: Session, slug: str) -> FoodDetail:
    item = await repository.get_by_slug(session, slug)
    if item is None:
        raise HTTPException(status_code=404, detail="food not found")
    return FoodDetail.of(item)
