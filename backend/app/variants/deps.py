"""``optional_user``: the signed-in user when a bearer token is sent, else ``None``."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import current_user
from app.core.config import Settings, get_settings
from app.core.db import get_session
from app.users.models import User

_bearer = HTTPBearer(auto_error=False)


async def optional_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> User | None:
    """A bad or expired token is still a 401: it never silently becomes anonymous."""
    if credentials is None:
        return None
    return await current_user(credentials, session, settings)


OptionalUser = Annotated[User | None, Depends(optional_user)]
