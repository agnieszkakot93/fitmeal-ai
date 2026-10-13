"""Sign in with Apple identity token verification.

The token is an RS256 JWT signed with one of Apple's keys (JWKS). We check the
signature, ``iss``, ``aud`` (our client ids), ``exp`` and the nonce. Keys are
cached; an unknown ``kid`` triggers at most one refetch per ``min_refetch_s`` so
forged tokens can't make us hammer Apple.
"""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import time
from dataclasses import dataclass
from typing import Any

import httpx
import jwt

APPLE_ISSUER = "https://appleid.apple.com"
_RELAY_DOMAIN = "@privaterelay.appleid.com"


class InvalidAppleToken(Exception):
    """The identity token is not one we accept. The message is safe to log."""


class AppleUnavailable(Exception):
    """Apple's keys could not be fetched and none are cached."""


@dataclass(frozen=True)
class AppleIdentity:
    sub: str
    # only a private-relay address; a real address is dropped (data minimization)
    email_relay: str | None


class AppleKeys:
    """Apple's signing keys, cached for ``ttl_s``."""

    def __init__(
        self,
        url: str,
        *,
        ttl_s: float = 24 * 3600,
        min_refetch_s: float = 60,
        timeout_s: float = 5,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._url = url
        self._ttl_s = ttl_s
        self._min_refetch_s = min_refetch_s
        self._timeout_s = timeout_s
        self._transport = transport
        self._keys: dict[str, jwt.PyJWK] = {}
        self._fetched_at: float | None = None
        self._lock = asyncio.Lock()

    async def get(self, kid: str) -> jwt.PyJWK:
        async with self._lock:
            now = time.monotonic()
            age = None if self._fetched_at is None else now - self._fetched_at
            if (
                age is None
                or age >= self._ttl_s
                or (kid not in self._keys and age >= self._min_refetch_s)
            ):
                await self._refresh(now)
            key = self._keys.get(kid)
        if key is None:
            raise InvalidAppleToken("unknown signing key")
        return key

    async def _refresh(self, now: float) -> None:
        try:
            async with httpx.AsyncClient(
                timeout=self._timeout_s, follow_redirects=False, transport=self._transport
            ) as client:
                res = await client.get(self._url)
                res.raise_for_status()
                keys = _parse_jwks(res.json())
        except (httpx.HTTPError, ValueError, jwt.PyJWKError) as exc:
            if not self._keys:
                raise AppleUnavailable("could not fetch Apple keys") from exc
            # keep serving the cached keys; try again after min_refetch_s
            self._fetched_at = now - self._ttl_s + self._min_refetch_s
            return
        self._keys = keys
        self._fetched_at = now


def _parse_jwks(body: Any) -> dict[str, jwt.PyJWK]:
    if not isinstance(body, dict) or not isinstance(body.get("keys"), list):
        raise ValueError("not a JWKS")
    keys: dict[str, jwt.PyJWK] = {}
    for jwk in body["keys"]:
        if isinstance(jwk, dict) and jwk.get("kty") == "RSA" and isinstance(jwk.get("kid"), str):
            keys[jwk["kid"]] = jwt.PyJWK(jwk, algorithm="RS256")
    return keys


class AppleVerifier:
    def __init__(self, keys: AppleKeys, client_ids: list[str], leeway_s: float = 30) -> None:
        self._keys = keys
        self._client_ids = list(client_ids)
        self._leeway_s = leeway_s

    async def verify(self, token: str, nonce: str | None) -> AppleIdentity:
        if not self._client_ids:
            # no bundle id configured: accept nothing rather than any audience
            raise InvalidAppleToken("no Apple client id configured")
        try:
            header = jwt.get_unverified_header(token)
        except jwt.PyJWTError as exc:
            raise InvalidAppleToken("malformed token") from exc
        kid = header.get("kid")
        if header.get("alg") != "RS256" or not isinstance(kid, str):
            raise InvalidAppleToken("unexpected token header")
        key = await self._keys.get(kid)
        try:
            claims: dict[str, Any] = jwt.decode(
                token,
                key=key.key,
                algorithms=["RS256"],
                audience=self._client_ids,
                issuer=APPLE_ISSUER,
                leeway=self._leeway_s,
                options={"require": ["iss", "aud", "exp", "iat", "sub"]},
            )
        except jwt.PyJWTError as exc:
            raise InvalidAppleToken(type(exc).__name__) from exc
        _check_nonce(claims.get("nonce"), nonce)
        sub = claims["sub"]
        if not isinstance(sub, str) or not 0 < len(sub) <= 255:
            raise InvalidAppleToken("bad subject")
        return AppleIdentity(sub=sub, email_relay=_relay_email(claims))


def _check_nonce(claimed: Any, raw: str | None) -> None:
    """The app sends Apple sha256(raw nonce) and sends us the raw nonce.

    A token that carries a nonce is only accepted with its raw nonce, so a
    stolen token can't be replayed by someone who doesn't have it.
    """
    if claimed is None and raw is None:
        return
    if claimed is None or raw is None or not isinstance(claimed, str):
        raise InvalidAppleToken("nonce mismatch")
    expected = hashlib.sha256(raw.encode()).hexdigest()
    if not hmac.compare_digest(expected, claimed):
        raise InvalidAppleToken("nonce mismatch")


def _relay_email(claims: dict[str, Any]) -> str | None:
    email = claims.get("email")
    private = claims.get("is_private_email") in (True, "true")
    if private and isinstance(email, str) and email.lower().endswith(_RELAY_DOMAIN):
        return email.lower()
    return None
