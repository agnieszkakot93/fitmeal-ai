"""Request and response schemas for the shopping list API."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.foods.vocab import FoodCategory
from app.shopping.aggregate import Lang
from app.shopping.display import DisplayUnit


class AmountOut(BaseModel):
    value: float = Field(description="Whole except for kg and l, which have one decimal")
    unit: DisplayUnit


class PackageCountOut(BaseModel):
    size_g: int
    count: int


class PackagesOut(BaseModel):
    buy: list[PackageCountOut] = Field(description="Package sizes to buy, largest first")
    count: int
    total_g: int
    leftover_g: float


class ShoppingItemOut(BaseModel):
    id: uuid.UUID = Field(description="Stable across regenerations while the food stays listed")
    food_slug: str
    name: str = Field(description="In the list's language")
    category: FoodCategory
    grams: float = Field(description="The exact total over the plan")
    amount: AmountOut = Field(description="Rounded up for display")
    packages: PackagesOut | None = Field(description="None when no package sizes are known")
    checked: bool
    checked_updated_at: datetime | None


class SectionOut(BaseModel):
    category: FoodCategory
    items: list[ShoppingItemOut]


class ShoppingListOut(BaseModel):
    plan_id: uuid.UUID
    lang: Lang
    sections: list[SectionOut] = Field(description="Store sections in store-walk order")


class ShoppingItemCheckIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    checked: bool
    event_id: uuid.UUID = Field(
        description="Client-generated, unique per change: a replay with the same id is a no-op"
    )
