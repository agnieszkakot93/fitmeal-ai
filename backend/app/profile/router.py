"""``GET/PUT /v1/me/profile``: the health profile stored in the account (D13).

Both need an active ``health_data`` consent (GDPR Art. 9(2)(a)); without one
they answer 403 ``health_data_consent_required``. Withdrawing the consent
deletes the profile (:mod:`app.users.repository`).
"""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import CurrentUser
from app.auth.routing import HideInputRoute
from app.core.db import get_session
from app.profile import repository, service
from app.profile.schemas import HealthProfileIn, HealthProfileOut

router = APIRouter(prefix="/v1/me/profile", tags=["profile"], route_class=HideInputRoute)

Session = Annotated[AsyncSession, Depends(get_session)]

_ERRORS: dict[int | str, dict[str, Any]] = {
    status.HTTP_403_FORBIDDEN: {"description": f"`{service.CONSENT_REQUIRED}`: no active consent"},
    status.HTTP_503_SERVICE_UNAVAILABLE: {
        "description": f"`{service.UNAVAILABLE}`: the encryption key is not available"
    },
}


@router.get(
    "",
    response_model=HealthProfileOut,
    responses={**_ERRORS, status.HTTP_404_NOT_FOUND: {"description": "No profile saved yet"}},
)
async def get_profile(user: CurrentUser, session: Session) -> HealthProfileOut:
    if not await repository.has_health_consent(session, user.id):
        raise service.consent_required()
    profile = await service.load(session, user.id)
    if profile is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "profile not found")
    return profile


@router.put("", response_model=HealthProfileOut, responses=_ERRORS)
async def put_profile(
    body: HealthProfileIn, user: CurrentUser, session: Session
) -> HealthProfileOut:
    """Save the whole profile, replacing the stored one."""
    user_id = user.id
    await repository.lock_user(session, user_id)
    if not await repository.has_health_consent(session, user_id):
        await session.rollback()
        raise service.consent_required()
    await repository.put(session, service.cipher(), user_id, body)
    await session.commit()
    saved = await service.load(session, user_id)
    assert saved is not None
    return saved
