from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.profile.schemas import HealthProfileOut
from app.users.models import ConsentType


class ConsentIn(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True)

    type: ConsentType
    # version of the consent text shown, e.g. "2026-10-01" or "1.2"
    version: str = Field(pattern=r"^[A-Za-z0-9._-]{1,32}$")
    granted: bool


class ConsentsIn(BaseModel):
    """Answers from one consent screen, recorded together."""

    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True)

    consents: list[ConsentIn] = Field(min_length=1, max_length=len(ConsentType))

    @model_validator(mode="after")
    def _one_answer_per_type(self) -> Self:
        # answers share one timestamp, so two for a type would leave the current one undefined
        if len({c.type for c in self.consents}) != len(self.consents):
            raise ValueError("one answer per consent type")
        return self


class ConsentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: ConsentType
    version: str
    granted: bool
    recorded_at: datetime


class MeOut(BaseModel):
    id: uuid.UUID
    created_at: datetime
    email_relay: str | None
    # the latest answer per consent type
    consents: list[ConsentOut]


class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    expires_at: datetime
    used_at: datetime | None
    revoked_at: datetime | None


class ExportOut(BaseModel):
    """Everything the server stores about the user (GDPR Art. 15 and 20).

    The health profile is decrypted here (D13); ``None`` when none is stored.
    """

    exported_at: datetime
    user: MeOut
    consent_history: list[ConsentOut]
    # refresh tokens, without their hashes
    sessions: list[SessionOut]
    health_profile: HealthProfileOut | None
    private_recipes: list[dict[str, Any]]
    recipe_variants: list[dict[str, Any]]
    # each with its slots, and each slot with its status events
    plans: list[dict[str, Any]]
