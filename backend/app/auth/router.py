from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import service
from app.auth.apple import AppleUnavailable, AppleVerifier, InvalidAppleToken
from app.auth.deps import get_apple_verifier
from app.auth.routing import HideInputRoute
from app.auth.schemas import AppleLoginIn, RefreshIn, TokenPair
from app.core.config import Settings, get_settings
from app.core.db import get_session

router = APIRouter(prefix="/v1/auth", tags=["auth"], route_class=HideInputRoute)

Session = Annotated[AsyncSession, Depends(get_session)]
Config = Annotated[Settings, Depends(get_settings)]


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status.HTTP_401_UNAUTHORIZED, detail=detail, headers={"WWW-Authenticate": "Bearer"}
    )


@router.post("/apple", response_model=TokenPair)
async def sign_in_with_apple(
    body: AppleLoginIn,
    session: Session,
    settings: Config,
    verifier: Annotated[AppleVerifier, Depends(get_apple_verifier)],
) -> TokenPair:
    """Exchange an Apple identity token for our access and refresh tokens."""
    try:
        identity = await verifier.verify(body.identity_token, body.nonce)
    except InvalidAppleToken:
        raise _unauthorized("invalid identity token") from None
    except AppleUnavailable:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, detail="sign in unavailable, try again"
        ) from None
    user_id = await service.upsert_user(session, identity)
    pair = await service.issue_pair(session, user_id, settings)
    await session.commit()
    return pair


@router.post("/refresh", response_model=TokenPair)
async def refresh(body: RefreshIn, session: Session, settings: Config) -> TokenPair:
    """Rotate a refresh token. Each one works once; reusing one ends the session."""
    try:
        return await service.rotate(session, body.refresh_token, settings)
    except service.InvalidRefreshToken:
        raise _unauthorized("invalid refresh token") from None
