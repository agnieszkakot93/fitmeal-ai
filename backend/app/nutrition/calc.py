"""Recipe-level nutrition: ingredient lines → totals and per-serving values."""

from __future__ import annotations

from dataclasses import dataclass

from app.nutrition.nutrients import Nutrients, for_grams
from app.nutrition.units import FoodUnitData, to_grams


@dataclass(frozen=True, slots=True)
class FoodFacts:
    key: str
    per_100g: Nutrients
    units: FoodUnitData


@dataclass(frozen=True, slots=True)
class IngredientLine:
    food: FoodFacts
    amount: float
    unit: str


@dataclass(frozen=True, slots=True)
class LineResult:
    food_key: str
    grams: float
    nutrients: Nutrients


@dataclass(frozen=True, slots=True)
class RecipeNutrition:
    lines: list[LineResult]
    total: Nutrients
    per_serving: Nutrients
    total_grams: float


def calculate(lines: list[IngredientLine], servings: int = 1) -> RecipeNutrition:
    if servings < 1:
        raise ValueError("servings must be at least 1")
    results = []
    for line in lines:
        grams = to_grams(line.amount, line.unit, line.food.units)
        results.append(LineResult(line.food.key, grams, for_grams(line.food.per_100g, grams)))
    total = Nutrients.total([r.nutrients for r in results])
    return RecipeNutrition(
        lines=results,
        total=total,
        per_serving=total.scale(1 / servings),
        total_grams=sum(r.grams for r in results),
    )
