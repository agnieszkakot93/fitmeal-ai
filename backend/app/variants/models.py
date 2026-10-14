"""Which saved variant a plan slot is cooked from (Development Plan §4, §9 S6).

The variant itself is a ``recipe_variants`` row (:class:`app.recipes.models.RecipeVariant`).
A slot has at most one; swapping the slot's recipe drops the link. Both sides
cascade, so deleting a plan or a variant (or the account) removes the link.
"""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.plans import models as _plans  # noqa: F401  (the tables the foreign keys name)
from app.recipes import models as _recipes  # noqa: F401


class PlanSlotVariant(Base):
    __tablename__ = "plan_slot_variants"

    slot_id: Mapped[int] = mapped_column(
        ForeignKey("plan_slots.id", ondelete="CASCADE"), primary_key=True
    )
    variant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("recipe_variants.id", ondelete="CASCADE"), index=True
    )
