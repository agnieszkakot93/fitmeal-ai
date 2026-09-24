"""Nutrition for an ad-hoc ingredient list (used by import previews and for QA)."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.foods import repository
from app.foods.schemas import NutrientsOut
from app.nutrition.calc import IngredientLine, calculate
from app.nutrition.nutrients import Nutrients
from app.nutrition.units import UnitConversionError

router = APIRouter(prefix="/v1/nutrition", tags=["nutrition"])


class IngredientIn(BaseModel):
    food: str = Field(description="Food slug")
    amount: float = Field(ge=0)
    unit: str = Field(min_length=1, max_length=30)


class CalculateIn(BaseModel):
    servings: int = Field(default=1, ge=1, le=50)
    ingredients: list[IngredientIn] = Field(min_length=1, max_length=100)


class LineOut(BaseModel):
    food: str
    grams: float
    nutrients: NutrientsOut


class CalculateOut(BaseModel):
    lines: list[LineOut]
    total: NutrientsOut
    per_serving: NutrientsOut
    total_grams: float


def _out(n: Nutrients) -> NutrientsOut:
    r = n.rounded()
    return NutrientsOut(
        kcal=r.kcal, protein_g=r.protein_g, fat_g=r.fat_g, carbs_g=r.carbs_g, fiber_g=r.fiber_g
    )


@router.post("/calculate", response_model=CalculateOut)
async def calculate_nutrition(
    body: CalculateIn, session: Annotated[AsyncSession, Depends(get_session)]
) -> CalculateOut:
    foods = await repository.get_by_slugs(session, [i.food for i in body.ingredients])
    errors: list[dict[str, object]] = []
    lines: list[IngredientLine] = []
    for index, ing in enumerate(body.ingredients):
        item = foods.get(ing.food)
        if item is None:
            errors.append({"index": index, "food": ing.food, "error": "unknown food"})
            continue
        lines.append(IngredientLine(repository.to_facts(item), ing.amount, ing.unit))

    result = None
    if not errors:
        try:
            result = calculate(lines, servings=body.servings)
        except UnitConversionError:
            # Find every line that fails, so the client can ask about all of them at once.
            for index, line in enumerate(lines):
                try:
                    calculate([line])
                except UnitConversionError as exc:
                    errors.append({"index": index, "food": line.food.key, "error": str(exc)})
    if errors or result is None:
        raise HTTPException(status_code=422, detail=errors)

    return CalculateOut(
        lines=[
            LineOut(food=r.food_key, grams=round(r.grams, 1), nutrients=_out(r.nutrients))
            for r in result.lines
        ],
        total=_out(result.total),
        per_serving=_out(result.per_serving),
        total_grams=round(result.total_grams, 1),
    )
