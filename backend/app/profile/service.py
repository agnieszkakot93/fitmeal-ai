"""The profile as the HTTP endpoints use it: the consent gate and fail-closed key errors.

Used by ``/v1/me/profile``, the data export and ``POST /v1/plans``.
"""

from __future__ import annotations

import logging
import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.plans.schemas import ProfileIn
from app.profile import repository
from app.profile.crypto import DecryptionFailed, KeyUnavailable, ProfileCipher, get_cipher
from app.profile.schemas import HealthProfileOut

log = logging.getLogger(__name__)

CONSENT_REQUIRED = "health_data_consent_required"
UNAVAILABLE = "health_profile_unavailable"


def consent_required() -> HTTPException:
    return HTTPException(status.HTTP_403_FORBIDDEN, CONSENT_REQUIRED)


def cipher() -> ProfileCipher:
    """The cipher, or a 503: without a usable key nothing is read or written."""
    try:
        return get_cipher()
    except KeyUnavailable as exc:
        # the reason names a setting, never a value
        log.error("health profile key unavailable: %s", exc)
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, UNAVAILABLE) from None


async def load(session: AsyncSession, user_id: uuid.UUID) -> HealthProfileOut | None:
    """The decrypted profile, ``None`` if there is none; 503 if it can't be decrypted."""
    if not await repository.exists(session, user_id):
        return None
    try:
        return await repository.get(session, cipher(), user_id)
    except (KeyUnavailable, DecryptionFailed) as exc:
        log.error("health profile of a user could not be decrypted: %s", type(exc).__name__)
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, UNAVAILABLE) from None


async def for_planning(session: AsyncSession, user_id: uuid.UUID) -> ProfileIn | None:
    """The stored profile if there is one and health-data consent is active, else ``None``."""
    if not await repository.has_health_consent(session, user_id):
        return None
    return await load(session, user_id)
