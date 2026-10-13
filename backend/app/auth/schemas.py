from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class _In(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True)


class AppleLoginIn(_In):
    identity_token: str = Field(min_length=1, max_length=8192)
    # the raw nonce; the app passed sha256(nonce) to Apple
    nonce: str | None = Field(default=None, min_length=1, max_length=256)


class RefreshIn(_In):
    refresh_token: str = Field(min_length=1, max_length=256)


class TokenPair(BaseModel):
    access_token: str
    # Left out of the body when the refresh token travels in the HttpOnly cookie (web).
    refresh_token: str | None = None
    token_type: Literal["bearer"] = "bearer"
    # seconds until the access token expires
    expires_in: int
    refresh_expires_in: int
