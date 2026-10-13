"""``current_user``: the dependency every authenticated endpoint uses."""

from __future__ import annotations

from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import tokens
from app.auth.apple import AppleKeys, AppleVerifier
from app.core.config import Settings, get_settings
from app.core.db import get_session
from app.users.models import User

_bearer = HTTPBearer(auto_error=False)

_UNAUTHORIZED = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)


async def current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> User:
    if credentials is None:
        raise _UNAUTHORIZED
    try:
        user_id = tokens.decode_access(credentials.credentials, settings)
    except tokens.InvalidAccessToken:
        raise _UNAUTHORIZED from None
    # a deleted account's access token stops working at once
    user = await session.get(User, user_id)
    if user is None:
        raise _UNAUTHORIZED
    return user


CurrentUser = Annotated[User, Depends(current_user)]


@lru_cache
def get_apple_verifier() -> AppleVerifier:
    settings = get_settings()
    return AppleVerifier(AppleKeys(settings.apple_jwks_url), settings.apple_client_ids)
