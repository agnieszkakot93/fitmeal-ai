"""Recipe schema (PRD §8.2, Development Plan §4).

Nutrition on a recipe is a cache of ``app.nutrition.calc`` over its
ingredients (``repository.refresh_nutrition``); it is never typed by hand.
Source-stated nutrition is kept on ``RecipeSource`` for comparison only.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from sqlalchemy import (
    ARRAY,
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.foods.models import FoodItem


class SourceType(StrEnum):
    CATALOG = "catalog"
    LINK = "link"
    PDF = "pdf"
    TEXT = "text"


class PublicUsageStatus(StrEnum):
    # imports are always private (PRD §8.1); only Donut-owned recipes are public
    PRIVATE_ONLY = "private_only"
    PUBLIC = "public"


class Difficulty(StrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


def _in(column: str, enum: type[StrEnum]) -> str:
    return f"{column} IN ({', '.join(f"'{e.value}'" for e in enum)})"


class RecipeSource(Base):
    __tablename__ = "recipe_sources"
    __table_args__ = (
        CheckConstraint(_in("type", SourceType), name="type_valid"),
        CheckConstraint(_in("public_usage_status", PublicUsageStatus), name="usage_valid"),
        CheckConstraint(
            "type = 'catalog' OR public_usage_status = 'private_only'",
            name="imports_private",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    type: Mapped[str] = mapped_column(Text)
    # URL for links, file name for PDFs, None for catalog and pasted text
    reference: Mapped[str | None] = mapped_column(Text)
    # sha256 of the imported text, to spot re-imports
    content_hash: Mapped[str | None] = mapped_column(Text)
    public_usage_status: Mapped[str] = mapped_column(
        Text, server_default=PublicUsageStatus.PRIVATE_ONLY.value
    )
    # nutrition as the source states it; for comparison only, never used
    stated_nutrition: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Recipe(Base):
    __tablename__ = "recipes"
    __table_args__ = (
        CheckConstraint("title_en IS NOT NULL OR title_pl IS NOT NULL", name="has_title"),
        CheckConstraint("servings >= 1", name="servings_positive"),
        CheckConstraint("prep_minutes >= 0 AND cook_minutes >= 0", name="times_non_negative"),
        CheckConstraint(_in("difficulty", Difficulty), name="difficulty_valid"),
        CheckConstraint("fridge_days >= 0", name="fridge_days_non_negative"),
        CheckConstraint("meal_prep_score BETWEEN 0 AND 100", name="meal_prep_score_range"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    # stable key for catalog recipes; None for imports
    slug: Mapped[str | None] = mapped_column(Text, unique=True)
    source_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("recipe_sources.id", ondelete="RESTRICT")
    )
    # owner of a private import; None for catalog recipes. No users table yet.
    owner_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), index=True)

    title_en: Mapped[str | None] = mapped_column(Text)
    title_pl: Mapped[str | None] = mapped_column(Text)
    instructions_en: Mapped[list[str]] = mapped_column(ARRAY(Text), server_default="{}")
    instructions_pl: Mapped[list[str]] = mapped_column(ARRAY(Text), server_default="{}")

    servings: Mapped[int] = mapped_column(Integer)
    prep_minutes: Mapped[int | None] = mapped_column(Integer)
    cook_minutes: Mapped[int | None] = mapped_column(Integer)
    difficulty: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str]] = mapped_column(ARRAY(Text), server_default="{}")
    equipment: Mapped[list[str]] = mapped_column(ARRAY(Text), server_default="{}")

    fridge_days: Mapped[int | None] = mapped_column(Integer)
    freezer_friendly: Mapped[bool] = mapped_column(Boolean, server_default="false")
    meal_prep_score: Mapped[int | None] = mapped_column(Integer)

    # cached totals for the whole recipe, from refresh_nutrition; None until computed
    kcal: Mapped[float | None] = mapped_column(Float)
    protein_g: Mapped[float | None] = mapped_column(Float)
    fat_g: Mapped[float | None] = mapped_column(Float)
    carbs_g: Mapped[float | None] = mapped_column(Float)
    fiber_g: Mapped[float | None] = mapped_column(Float)
    total_grams: Mapped[float | None] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    source: Mapped[RecipeSource] = relationship()
    ingredients: Mapped[list[RecipeIngredient]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
        order_by="RecipeIngredient.position",
    )
    variants: Mapped[list[RecipeVariant]] = relationship(
        back_populates="base_recipe", cascade="all, delete-orphan"
    )


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    __table_args__ = (
        UniqueConstraint("recipe_id", "position"),
        CheckConstraint("amount_g > 0", name="amount_positive"),
        CheckConstraint("display_amount IS NULL OR display_amount > 0", name="display_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recipe_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"))
    position: Mapped[int] = mapped_column(Integer)
    food_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("food_items.id", ondelete="RESTRICT"), index=True
    )
    # resolved weight; nutrition is always computed from this
    amount_g: Mapped[float] = mapped_column(Float)
    # what the user sees, e.g. 2 "clove"; None shows grams
    display_amount: Mapped[float | None] = mapped_column(Float)
    display_unit: Mapped[str | None] = mapped_column(Text)
    culinary_role: Mapped[str | None] = mapped_column(Text)
    optional: Mapped[bool] = mapped_column(Boolean, server_default="false")
    prep_note: Mapped[str | None] = mapped_column(Text)

    recipe: Mapped[Recipe] = relationship(back_populates="ingredients")
    food: Mapped[FoodItem] = relationship()


class RecipeVariant(Base):
    """A personalization of a base recipe stored as a diff (PRD §10).

    Lineage: base recipe → shared variant (``user_id`` None, e.g. high-protein)
    → user's variant (``parent_variant_id`` set).
    """

    __tablename__ = "recipe_variants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    base_recipe_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"), index=True
    )
    parent_variant_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("recipe_variants.id", ondelete="CASCADE")
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), index=True)
    label: Mapped[str | None] = mapped_column(Text)
    # only the targets this variant was computed for, never the health profile
    targets: Mapped[dict[str, Any]] = mapped_column(JSONB, server_default="{}")
    ingredient_changes: Mapped[list[Any]] = mapped_column(JSONB, server_default="[]")
    nutrition: Mapped[dict[str, Any]] = mapped_column(JSONB, server_default="{}")
    instruction_overrides: Mapped[dict[str, Any]] = mapped_column(JSONB, server_default="{}")
    explanations: Mapped[list[Any]] = mapped_column(JSONB, server_default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    base_recipe: Mapped[Recipe] = relationship(back_populates="variants")
