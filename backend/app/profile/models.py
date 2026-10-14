"""The ``health_profiles`` table (Development Plan §4, D13).

One row per user. Every health field is stored as AES-GCM ciphertext
(:mod:`app.profile.crypto`); only the key id, the row version and the update
time are plain.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, LargeBinary, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base

# the encrypted columns, also the associated-data label of each
ENCRYPTED = ("targets", "body_data", "exclusions", "preferences")


class HealthProfile(Base):
    __tablename__ = "health_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    # daily kcal and protein minimum
    targets: Mapped[bytes] = mapped_column(LargeBinary)
    # optional age, sex, weight, height, activity level
    body_data: Mapped[bytes] = mapped_column(LargeBinary)
    # allergies, intolerances and dislikes with their tiers
    exclusions: Mapped[bytes] = mapped_column(LargeBinary)
    # meals and their calorie split, cooking time, equipment
    preferences: Mapped[bytes] = mapped_column(LargeBinary)
    # which key encrypted this row, for rotation
    key_id: Mapped[str] = mapped_column(Text)
    # bumped on every save (re-encryption under a new key leaves it and updated_at alone)
    version: Mapped[int] = mapped_column(Integer, default=1)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
