from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import service
from app.auth.apple import AppleUnavailable, AppleVerifier, InvalidAppleToken
from app.auth.cookies import (
    REFRESH_COOKIE,
    clear_refresh_cookie,
    clear_refresh_cookie_header,
    set_refresh_cookie,
)
from app.auth.deps import get_apple_verifier
from app.auth.routing import HideInputRoute
from app.auth.schemas import AppleLoginIn, RefreshIn, TokenPair
from app.core.config import Settings, get_settings
from app.core.db import get_session

router = APIRouter(prefix="/v1/auth", tags=["auth"], route_class=HideInputRoute)

Session = Annotated[AsyncSession, Depends(get_session)]
Config = Annotated[Settings, Depends(get_settings)]
RefreshCookie = Annotated[str | None, Cookie(alias=REFRESH_COOKIE, include_in_schema=False)]
# same bound as RefreshIn.refresh_token
MAX_REFRESH_TOKEN_LEN = 256


def _unauthorized(detail: str, *, clear_cookie: bool = False) -> HTTPException:
    headers = {"WWW-Authenticate": "Bearer"}
    if clear_cookie:
        headers["Set-Cookie"] = clear_refresh_cookie_header()
    return HTTPException(status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers)


def _presented(body: RefreshIn | None, cookie: str | None) -> tuple[str | None, bool]:
    """The refresh token and whether it came from the cookie. The body wins (iOS)."""
    if body is not None:
        return body.refresh_token, False
    if cookie and len(cookie) <= MAX_REFRESH_TOKEN_LEN:
        return cookie, True
    return None, cookie is not None


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


@router.post("/refresh", response_model=TokenPair, response_model_exclude_none=True)
async def refresh(
    response: Response,
    session: Session,
    settings: Config,
    cookie: RefreshCookie = None,
    body: RefreshIn | None = None,
) -> TokenPair:
    """Rotate a refresh token. Each one works once; reusing one ends the session.

    iOS sends the token in the body and gets the next one in the body. The web
    sends no body: the token comes from the HttpOnly cookie, the next one goes
    back in the cookie, and the response body carries only the access token.
    """
    presented, via_cookie = _presented(body, cookie)
    if presented is None:
        raise _unauthorized("missing refresh token", clear_cookie=via_cookie)
    try:
        pair = await service.rotate(session, presented, settings)
    except service.InvalidRefreshToken:
        raise _unauthorized("invalid refresh token", clear_cookie=via_cookie) from None
    if not via_cookie:
        return pair
    if pair.refresh_token is not None:  # always set by rotate(); narrows the type
        set_refresh_cookie(response, pair.refresh_token, pair.refresh_expires_in)
    return pair.model_copy(update={"refresh_token": None})


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    session: Session, cookie: RefreshCookie = None, body: RefreshIn | None = None
) -> Response:
    """Sign out this device: revoke its refresh token family and clear the cookie.

    Always 204, so it also works with an unknown or already revoked token.
    """
    presented, _ = _presented(body, cookie)
    if presented is not None:
        await service.revoke(session, presented)
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    clear_refresh_cookie(response)
    return response
