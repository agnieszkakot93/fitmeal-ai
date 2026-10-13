"""Account and consent tables (Development Plan §7.1).

Only what the account needs: the Apple subject, an optional Apple private-relay
address and the consent history. The health profile stays on the phone (D8).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class ConsentType(StrEnum):
    # explicit consent to health data processing, GDPR Art. 9(2)(a)
    HEALTH_DATA = "health_data"
    # the 18+ confirmation from onboarding (PRD §7)
    AGE_18_PLUS = "age_18_plus"
    TERMS_OF_USE = "terms_of_use"
    PRIVACY_POLICY = "privacy_policy"


def _in(column: str, enum: type[StrEnum]) -> str:
    return f"{column} IN ({', '.join(f"'{e.value}'" for e in enum)})"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    # Apple's stable user id for our team
    apple_sub: Mapped[str] = mapped_column(Text, unique=True)
    # set only when Apple sends a private-relay address; real addresses are not kept
    email_relay: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ConsentRecord(Base):
    """One answer on the consent screen. Append-only: a withdrawal is a new row."""

    __tablename__ = "consent_records"
    __table_args__ = (CheckConstraint(_in("type", ConsentType), name="type_valid"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    type: Mapped[str] = mapped_column(Text)
    # version of the text the user was shown
    version: Mapped[str] = mapped_column(Text)
    granted: Mapped[bool] = mapped_column(Boolean)
    # server time; the client's clock is not trusted
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
