"""Plan tables (Development Plan §4, §9 S5).

A plan keeps only what it needs to be shown and cooked: the recipes, portions,
the nutrition they add up to and the daily targets it was built for. The
profile it was built from (exclusions, body data) is never stored here (D8,
D13), and neither are the soft-exclusion labels, which would reveal it.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum

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
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.planner.inputs import MealType
from app.recipes.models import Recipe


class SlotStatus(StrEnum):
    PLANNED = "planned"
    COOKED = "cooked"
    EATEN = "eaten"
    SKIPPED = "skipped"


def _in(column: str, enum: type[StrEnum]) -> str:
    return f"{column} IN ({', '.join(f"'{e.value}'" for e in enum)})"


class MealPlan(Base):
    __tablename__ = "plans"
    __table_args__ = (
        CheckConstraint("days >= 1", name="days_positive"),
        CheckConstraint("prep_days >= 1", name="prep_days_positive"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    days: Mapped[int] = mapped_column(Integer)
    prep_days: Mapped[int] = mapped_column(Integer)
    # the daily targets the plan was built for, as recipe_variants.targets
    daily_kcal: Mapped[float] = mapped_column(Float)
    protein_min_g: Mapped[float] = mapped_column(Float)
    # soft goals that had to be relaxed, in plain words, and the rules behind them
    notices: Mapped[list[str]] = mapped_column(ARRAY(Text), server_default="{}")
    relaxed: Mapped[list[str]] = mapped_column(ARRAY(Text), server_default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    slots: Mapped[list[PlanSlot]] = relationship(
        back_populates="plan", cascade="all, delete-orphan", order_by="PlanSlot.position"
    )


class PlanSlot(Base):
    """One meal of one plan day: a recipe at a portion."""

    __tablename__ = "plan_slots"
    __table_args__ = (
        UniqueConstraint("plan_id", "position", name="uq_plan_slots_plan_id_position"),
        UniqueConstraint("plan_id", "day", "slot", name="uq_plan_slots_plan_id_day_slot"),
        CheckConstraint(_in("meal_type", MealType), name="meal_type_valid"),
        CheckConstraint(_in("status", SlotStatus), name="status_valid"),
        CheckConstraint("portion > 0", name="portion_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("plans.id", ondelete="CASCADE"))
    # the slot's address in the API: day by day, meals in profile order
    position: Mapped[int] = mapped_column(Integer)
    day: Mapped[int] = mapped_column(Integer)  # 0-based
    slot: Mapped[str] = mapped_column(Text)
    meal_type: Mapped[str] = mapped_column(Text)
    # SET NULL: erasing an account deletes its private recipes before the user row
    recipe_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("recipes.id", ondelete="SET NULL"), index=True
    )
    portion: Mapped[float] = mapped_column(Float)  # servings of the recipe
    # the portion's nutrition when planned, from the nutrition engine
    kcal: Mapped[float] = mapped_column(Float)
    protein_g: Mapped[float] = mapped_column(Float)
    fat_g: Mapped[float] = mapped_column(Float)
    carbs_g: Mapped[float] = mapped_column(Float)
    fiber_g: Mapped[float] = mapped_column(Float)
    cook_day: Mapped[int] = mapped_column(Integer)
    eat_by_day: Mapped[int] = mapped_column(Integer)
    from_batch: Mapped[bool] = mapped_column(Boolean)
    # optional ingredient keys to leave out when cooking
    leave_out: Mapped[list[str]] = mapped_column(ARRAY(Text), server_default="{}")
    status: Mapped[str] = mapped_column(Text, server_default=SlotStatus.PLANNED.value)
    status_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    plan: Mapped[MealPlan] = relationship(back_populates="slots")
    recipe: Mapped[Recipe | None] = relationship()


class SlotEvent(Base):
    """A meal status change as the client sent it.

    ``id`` is the client's event id: an offline outbox replaying the same event
    finds it here and changes nothing.
    """

    __tablename__ = "plan_slot_events"
    __table_args__ = (CheckConstraint(_in("status", SlotStatus), name="status_valid"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    slot_id: Mapped[int] = mapped_column(
        ForeignKey("plan_slots.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[str] = mapped_column(Text)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
