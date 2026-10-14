"""Shopping list tables (Development Plan §9 S8).

One row per food on a plan's list, so a checkmark survives regenerating the
list. The amounts shown are computed from ``grams`` and the food database on
every read; only the total and the checkmark are stored.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.foods.models import FoodItem


class ShoppingListItem(Base):
    __tablename__ = "shopping_items"
    __table_args__ = (
        UniqueConstraint("plan_id", "food_id", name="uq_shopping_items_plan_id_food_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    plan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("plans.id", ondelete="CASCADE"))
    # the list is rebuilt from the plan, so a deleted food just drops off it
    food_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("food_items.id", ondelete="CASCADE"), index=True
    )
    grams: Mapped[float] = mapped_column(Float)  # the exact total over the plan
    checked: Mapped[bool] = mapped_column(Boolean, server_default="false")
    checked_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    food: Mapped[FoodItem] = relationship()


class ShoppingItemEvent(Base):
    """A checkmark change as the client sent it.

    ``id`` is the client's event id: an offline outbox replaying the same event
    finds it here and changes nothing.
    """

    __tablename__ = "shopping_item_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("shopping_items.id", ondelete="CASCADE"), index=True
    )
    checked: Mapped[bool] = mapped_column(Boolean)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
