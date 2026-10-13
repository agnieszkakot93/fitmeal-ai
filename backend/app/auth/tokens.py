"""Our tokens: a short-lived access JWT and an opaque, rotating refresh token."""

from __future__ import annotations

import hashlib
import secrets
import uuid
from datetime import UTC, datetime, timedelta

import jwt

from app.core.config import DEV_JWT_SECRET, Settings

ISSUER = "donut"
AUDIENCE = "donut-api"
_ALGORITHM = "HS256"
_MIN_SECRET_LEN = 32


class InvalidAccessToken(Exception):
    pass


def _secret(settings: Settings) -> str:
    secret = settings.jwt_secret.get_secret_value()
    if settings.env not in ("dev", "test") and (
        secret == DEV_JWT_SECRET or len(secret) < _MIN_SECRET_LEN
    ):
        raise RuntimeError("DONUT_JWT_SECRET must be set to a random value of 32+ characters")
    return secret


def issue_access(user_id: uuid.UUID, settings: Settings, now: datetime | None = None) -> str:
    now = now or datetime.now(UTC)
    claims = {
        "sub": str(user_id),
        "iss": ISSUER,
        "aud": AUDIENCE,
        "typ": "access",
        "iat": now,
        "exp": now + timedelta(seconds=settings.access_token_ttl_s),
    }
    return jwt.encode(claims, _secret(settings), algorithm=_ALGORITHM)


def decode_access(token: str, settings: Settings) -> uuid.UUID:
    try:
        claims = jwt.decode(
            token,
            _secret(settings),
            algorithms=[_ALGORITHM],
            audience=AUDIENCE,
            issuer=ISSUER,
            options={"require": ["sub", "iss", "aud", "exp", "iat"]},
        )
        if claims.get("typ") != "access":
            raise InvalidAccessToken("not an access token")
        return uuid.UUID(claims["sub"])
    except (jwt.PyJWTError, ValueError, TypeError) as exc:
        raise InvalidAccessToken(type(exc).__name__) from exc


def new_refresh_token() -> str:
    return secrets.token_urlsafe(32)


def hash_refresh_token(token: str) -> str:
    # 256 random bits, so a fast hash is enough; the database never sees the token
    return hashlib.sha256(token.encode()).hexdigest()
