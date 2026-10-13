"""The web refresh token cookie (Development Plan §3.1).

The web client never sees its refresh token: it lives in an HttpOnly, Secure,
SameSite=Strict cookie scoped to /v1/auth, so it is sent only to the refresh
and logout calls and never to the rest of the API. iOS keeps the token in the
Keychain and sends it in the body instead.
"""

from __future__ import annotations

from fastapi import Response

REFRESH_COOKIE = "refresh_token"
COOKIE_PATH = "/v1/auth"


def set_refresh_cookie(response: Response, token: str, max_age: int) -> None:
    response.set_cookie(
        REFRESH_COOKIE,
        token,
        max_age=max_age,
        path=COOKIE_PATH,
        secure=True,
        httponly=True,
        samesite="strict",
    )


def clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(
        REFRESH_COOKIE, path=COOKIE_PATH, secure=True, httponly=True, samesite="strict"
    )


def clear_refresh_cookie_header() -> str:
    """The Set-Cookie value that clears the cookie, for error responses."""
    response = Response()
    clear_refresh_cookie(response)
    return response.headers["set-cookie"]
