from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    ARRAY,
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class FoodItem(Base):
    """A canonical ingredient. Nutrition is per 100 g; carbs exclude fiber."""

    __tablename__ = "food_items"
    __table_args__ = (
        CheckConstraint(
            "kcal >= 0 AND protein_g >= 0 AND fat_g >= 0 AND carbs_g >= 0 AND fiber_g >= 0",
            name="nutrients_non_negative",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    slug: Mapped[str] = mapped_column(Text, unique=True)
    name_en: Mapped[str] = mapped_column(Text)
    name_pl: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(Text)
    origin: Mapped[str] = mapped_column(Text)

    kcal: Mapped[float] = mapped_column(Float)
    protein_g: Mapped[float] = mapped_column(Float)
    fat_g: Mapped[float] = mapped_column(Float)
    carbs_g: Mapped[float] = mapped_column(Float)
    fiber_g: Mapped[float] = mapped_column(Float)
    water_g: Mapped[float | None] = mapped_column(Float)

    density_g_per_ml: Mapped[float | None] = mapped_column(Float)
    allergens: Mapped[list[str]] = mapped_column(ARRAY(Text), server_default="{}")
    # own allergens + everything inherited through food_derivations
    effective_allergens: Mapped[list[str]] = mapped_column(ARRAY(Text), server_default="{}")
    culinary_roles: Mapped[list[str]] = mapped_column(ARRAY(Text), server_default="{}")
    substitution_groups: Mapped[list[str]] = mapped_column(ARRAY(Text), server_default="{}")

    # nutrition source, e.g. ("usda_fdc", "171077") or ("label", "Piątnica skyr")
    source: Mapped[str] = mapped_column(Text)
    source_ref: Mapped[str | None] = mapped_column(Text)
    # a human has checked names, portions, density and allergens
    reviewed: Mapped[bool] = mapped_column(Boolean, server_default="false")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    aliases: Mapped[list[FoodAlias]] = relationship(
        back_populates="food", cascade="all, delete-orphan"
    )
    portions: Mapped[list[FoodPortion]] = relationship(
        back_populates="food", cascade="all, delete-orphan"
    )
    packages: Mapped[list[FoodPackage]] = relationship(
        back_populates="food", cascade="all, delete-orphan"
    )


class FoodDerivation(Base):
    __tablename__ = "food_derivations"

    food_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("food_items.id", ondelete="CASCADE"), primary_key=True
    )
    parent_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("food_items.id", ondelete="RESTRICT"), primary_key=True
    )


class FoodAlias(Base):
    __tablename__ = "food_aliases"
    __table_args__ = (
        UniqueConstraint("food_id", "lang", "alias_folded"),
        Index(
            "ix_food_aliases_alias_folded_trgm",
            "alias_folded",
            postgresql_using="gin",
            postgresql_ops={"alias_folded": "gin_trgm_ops"},
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    food_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("food_items.id", ondelete="CASCADE"))
    lang: Mapped[str] = mapped_column(Text)
    alias: Mapped[str] = mapped_column(Text)
    alias_folded: Mapped[str] = mapped_column(Text)

    food: Mapped[FoodItem] = relationship(back_populates="aliases")


class FoodPortion(Base):
    """Grams per portion unit (piece, clove, scoop ...) or per volume unit override."""

    __tablename__ = "food_portions"
    __table_args__ = (CheckConstraint("grams > 0", name="grams_positive"),)

    food_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("food_items.id", ondelete="CASCADE"), primary_key=True
    )
    unit: Mapped[str] = mapped_column(Text, primary_key=True)
    grams: Mapped[float] = mapped_column(Float)

    food: Mapped[FoodItem] = relationship(back_populates="portions")


class FoodPackage(Base):
    __tablename__ = "food_packages"
    __table_args__ = (CheckConstraint("size_g > 0", name="size_positive"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    food_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("food_items.id", ondelete="CASCADE"))
    size_g: Mapped[float] = mapped_column(Float)

    food: Mapped[FoodItem] = relationship(back_populates="packages")
