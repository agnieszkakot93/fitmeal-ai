"""Sign in with Apple and our token pair, against Postgres.

Apple's JWKS is served from a locally generated RSA key through an httpx mock
transport; nothing goes to the network.
"""

import asyncio
import hashlib
import json
import time
import uuid
from collections.abc import AsyncIterator, Iterator
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

import httpx
import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select, text

from app.auth import tokens
from app.auth.apple import APPLE_ISSUER, AppleKeys, AppleVerifier, InvalidAppleToken
from app.auth.deps import get_apple_verifier
from app.auth.models import RefreshToken
from app.core.config import get_settings
from app.core.db import get_sessionmaker
from app.main import app
from app.users.models import User

CLIENT_ID = "app.example.donut-test"
KID = "test-kid"
JWKS_URL = "https://apple.test/auth/keys"

Json = dict[str, Any]


def _rsa() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.fixture(scope="session")
def apple_key() -> rsa.RSAPrivateKey:
    return _rsa()


@dataclass
class FakeApple:
    key: rsa.RSAPrivateKey
    fetches: int = 0
    jwks: list[Json] = field(default_factory=list)

    def token(
        self,
        sub: str = "apple-sub-1",
        *,
        aud: str = CLIENT_ID,
        iss: str = APPLE_ISSUER,
        expires_in: int = 600,
        kid: str = KID,
        key: rsa.RSAPrivateKey | None = None,
        **claims: Any,
    ) -> str:
        now = datetime.now(UTC)
        payload = {
            "iss": iss,
            "aud": aud,
            "sub": sub,
            "iat": now,
            "exp": now + timedelta(seconds=expires_in),
            **claims,
        }
        return jwt.encode(payload, key or self.key, algorithm="RS256", headers={"kid": kid})

    def handler(self, request: httpx.Request) -> httpx.Response:
        assert str(request.url) == JWKS_URL
        self.fetches += 1
        return httpx.Response(200, json={"keys": self.jwks})


def _jwk(key: rsa.RSAPrivateKey, kid: str) -> Json:
    jwk: Json = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(key.public_key()))
    return {**jwk, "kid": kid, "alg": "RS256", "use": "sig"}


@pytest.fixture
def apple(apple_key: rsa.RSAPrivateKey) -> Iterator[FakeApple]:
    fake = FakeApple(apple_key, jwks=[_jwk(apple_key, KID)])
    keys = AppleKeys(JWKS_URL, transport=httpx.MockTransport(fake.handler))
    verifier = AppleVerifier(keys, [CLIENT_ID])
    app.dependency_overrides[get_apple_verifier] = lambda: verifier
    yield fake
    app.dependency_overrides.pop(get_apple_verifier, None)


@pytest.fixture
async def client(migrated_db: None, apple: FakeApple) -> AsyncIterator[AsyncClient]:
    async with get_sessionmaker()() as session:
        await session.execute(text("TRUNCATE users CASCADE"))
        await session.commit()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


async def login(client: AsyncClient, apple: FakeApple, sub: str = "apple-sub-1") -> Json:
    res = await client.post("/v1/auth/apple", json={"identity_token": apple.token(sub)})
    assert res.status_code == 200, res.text
    body: Json = res.json()
    return body


def bearer(pair: Json) -> dict[str, str]:
    return {"Authorization": f"Bearer {pair['access_token']}"}


async def _refresh(client: AsyncClient, token: str) -> httpx.Response:
    return await client.post("/v1/auth/refresh", json={"refresh_token": token})


async def _count(model: type[User] | type[RefreshToken]) -> int:
    async with get_sessionmaker()() as session:
        return int(await session.scalar(select(func.count()).select_from(model)) or 0)


# ── Sign in with Apple ──────────────────────────────────────────────────────


async def test_login_issues_a_pair_and_creates_the_user(
    client: AsyncClient, apple: FakeApple
) -> None:
    pair = await login(client, apple)
    assert pair["token_type"] == "bearer"
    assert pair["expires_in"] == 15 * 60
    me = await client.get("/v1/me", headers=bearer(pair))
    assert me.status_code == 200

    # the same Apple account signs in to the same user
    again = await login(client, apple)
    me_again = await client.get("/v1/me", headers=bearer(again))
    assert me_again.json()["id"] == me.json()["id"]
    assert await _count(User) == 1


async def test_access_token_lives_15_minutes(client: AsyncClient, apple: FakeApple) -> None:
    pair = await login(client, apple)
    claims = jwt.decode(pair["access_token"], options={"verify_signature": False})
    assert claims["exp"] - claims["iat"] == 15 * 60


async def test_refresh_token_is_stored_hashed(client: AsyncClient, apple: FakeApple) -> None:
    pair = await login(client, apple)
    async with get_sessionmaker()() as session:
        stored = (await session.scalars(select(RefreshToken))).one()
    assert stored.token_hash == hashlib.sha256(pair["refresh_token"].encode()).hexdigest()
    assert pair["refresh_token"] not in stored.token_hash


@pytest.mark.parametrize(
    "claims",
    [
        pytest.param({"aud": "com.someone.else"}, id="wrong-aud"),
        pytest.param({"iss": "https://evil.example"}, id="wrong-iss"),
        pytest.param({"expires_in": -120}, id="expired"),
        pytest.param({"kid": "unknown-kid"}, id="unknown-kid"),
    ],
)
async def test_login_rejects_bad_claims(
    client: AsyncClient, apple: FakeApple, claims: Json
) -> None:
    res = await client.post("/v1/auth/apple", json={"identity_token": apple.token(**claims)})
    assert res.status_code == 401
    assert await _count(User) == 0


async def test_login_rejects_a_bad_signature(client: AsyncClient, apple: FakeApple) -> None:
    forged = apple.token(key=_rsa())  # right kid, someone else's key
    res = await client.post("/v1/auth/apple", json={"identity_token": forged})
    assert res.status_code == 401


async def test_login_rejects_other_algorithms(client: AsyncClient, apple: FakeApple) -> None:
    now = int(time.time())
    claims = {"iss": APPLE_ISSUER, "aud": CLIENT_ID, "sub": "x", "iat": now, "exp": now + 600}
    unsigned = jwt.encode(claims, "", algorithm="none", headers={"kid": KID})
    hs256 = jwt.encode(claims, "k" * 32, algorithm="HS256", headers={"kid": KID})
    for token in (unsigned, hs256, "not-a-jwt"):
        res = await client.post("/v1/auth/apple", json={"identity_token": token})
        assert res.status_code == 401


async def test_nonce_must_match(client: AsyncClient, apple: FakeApple) -> None:
    raw = "raw-nonce-123"
    token = apple.token(nonce=hashlib.sha256(raw.encode()).hexdigest())
    ok = await client.post("/v1/auth/apple", json={"identity_token": token, "nonce": raw})
    assert ok.status_code == 200
    wrong = await client.post("/v1/auth/apple", json={"identity_token": token, "nonce": "other"})
    assert wrong.status_code == 401
    # a nonce-bound token can't be replayed without the raw nonce
    missing = await client.post("/v1/auth/apple", json={"identity_token": token})
    assert missing.status_code == 401
    # nor can a nonce be satisfied by a token that has none
    unbound = await client.post(
        "/v1/auth/apple", json={"identity_token": apple.token(), "nonce": raw}
    )
    assert unbound.status_code == 401


async def test_only_a_private_relay_email_is_kept(client: AsyncClient, apple: FakeApple) -> None:
    relay = apple.token("relay-user", email="abc@privaterelay.appleid.com", is_private_email="true")
    real = apple.token("real-user", email="jan@example.com", is_private_email=False)
    for token, expected in ((relay, "abc@privaterelay.appleid.com"), (real, None)):
        pair = (await client.post("/v1/auth/apple", json={"identity_token": token})).json()
        me = await client.get("/v1/me", headers=bearer(pair))
        assert me.json()["email_relay"] == expected


async def test_validation_errors_do_not_echo_tokens(client: AsyncClient, apple: FakeApple) -> None:
    secret = "x" * 9000  # over the size limit
    res = await client.post("/v1/auth/apple", json={"identity_token": secret})
    assert res.status_code == 422
    assert secret[:50] not in res.text
    res = await client.post("/v1/auth/refresh", json={"refresh_token": secret, "extra": secret})
    assert res.status_code == 422
    assert secret[:50] not in res.text


async def test_jwks_is_cached(client: AsyncClient, apple: FakeApple) -> None:
    await login(client, apple, "a")
    await login(client, apple, "b")
    assert apple.fetches == 1


async def test_unknown_kid_refetch_is_rate_limited(apple_key: rsa.RSAPrivateKey) -> None:
    fake = FakeApple(apple_key, jwks=[_jwk(apple_key, KID)])
    keys = AppleKeys(JWKS_URL, transport=httpx.MockTransport(fake.handler), min_refetch_s=3600)
    verifier = AppleVerifier(keys, [CLIENT_ID])
    await verifier.verify(fake.token(), None)
    for _ in range(5):
        with pytest.raises(InvalidAppleToken):
            await verifier.verify(fake.token(kid="rotated"), None)
    assert fake.fetches == 1


async def test_new_apple_key_is_picked_up(apple_key: rsa.RSAPrivateKey) -> None:
    fake = FakeApple(apple_key, jwks=[_jwk(apple_key, KID)])
    keys = AppleKeys(JWKS_URL, transport=httpx.MockTransport(fake.handler), min_refetch_s=0)
    verifier = AppleVerifier(keys, [CLIENT_ID])
    await verifier.verify(fake.token(), None)
    new_key = _rsa()
    fake.jwks.append(_jwk(new_key, "rotated"))
    identity = await verifier.verify(fake.token(kid="rotated", key=new_key), None)
    assert identity.sub == "apple-sub-1"


async def test_no_client_id_configured_accepts_nothing(apple_key: rsa.RSAPrivateKey) -> None:
    fake = FakeApple(apple_key, jwks=[_jwk(apple_key, KID)])
    verifier = AppleVerifier(AppleKeys(JWKS_URL, transport=httpx.MockTransport(fake.handler)), [])
    with pytest.raises(InvalidAppleToken):
        await verifier.verify(fake.token(), None)


async def test_apple_down_is_503(client: AsyncClient, apple_key: rsa.RSAPrivateKey) -> None:
    def down(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    verifier = AppleVerifier(AppleKeys(JWKS_URL, transport=httpx.MockTransport(down)), [CLIENT_ID])
    app.dependency_overrides[get_apple_verifier] = lambda: verifier
    fake = FakeApple(apple_key)
    res = await client.post("/v1/auth/apple", json={"identity_token": fake.token()})
    assert res.status_code == 503


# ── refresh rotation ────────────────────────────────────────────────────────


async def test_refresh_rotates(client: AsyncClient, apple: FakeApple) -> None:
    first = await login(client, apple)
    res = await _refresh(client, first["refresh_token"])
    assert res.status_code == 200
    second = res.json()
    assert second["refresh_token"] != first["refresh_token"]
    assert (await client.get("/v1/me", headers=bearer(second))).status_code == 200
    third = await _refresh(client, second["refresh_token"])
    assert third.status_code == 200


async def test_refresh_reuse_revokes_the_family(client: AsyncClient, apple: FakeApple) -> None:
    first = await login(client, apple)
    other_device = await login(client, apple)  # a separate family
    second = (await _refresh(client, first["refresh_token"])).json()

    # the spent token comes back: someone has a copy
    reused = await _refresh(client, first["refresh_token"])
    assert reused.status_code == 401
    # so the legitimate successor dies too
    assert (await _refresh(client, second["refresh_token"])).status_code == 401
    # other logins are untouched
    assert (await _refresh(client, other_device["refresh_token"])).status_code == 200


async def test_concurrent_refresh_spends_the_token_once(
    client: AsyncClient, apple: FakeApple
) -> None:
    pair = await login(client, apple)
    results = await asyncio.gather(*(_refresh(client, pair["refresh_token"]) for _ in range(5)))
    assert sorted(r.status_code for r in results) == [200, 401, 401, 401, 401]


async def test_refresh_rejects_unknown_and_expired(client: AsyncClient, apple: FakeApple) -> None:
    assert (await _refresh(client, "garbage")).status_code == 401
    pair = await login(client, apple)
    async with get_sessionmaker()() as session:
        await session.execute(
            text("UPDATE refresh_tokens SET expires_at = now() - interval '1 second'")
        )
        await session.commit()
    assert (await _refresh(client, pair["refresh_token"])).status_code == 401


async def test_access_token_is_not_a_refresh_token(client: AsyncClient, apple: FakeApple) -> None:
    pair = await login(client, apple)
    assert (await _refresh(client, pair["access_token"][:256])).status_code == 401
    me = await client.get("/v1/me", headers={"Authorization": f"Bearer {pair['refresh_token']}"})
    assert me.status_code == 401


# ── current_user ────────────────────────────────────────────────────────────


async def test_me_requires_a_valid_access_token(client: AsyncClient, apple: FakeApple) -> None:
    assert (await client.get("/v1/me")).status_code == 401
    res = await client.get("/v1/me", headers={"Authorization": "Bearer nope"})
    assert res.status_code == 401
    assert res.headers["www-authenticate"] == "Bearer"

    pair = await login(client, apple)
    user_id = uuid.UUID((await client.get("/v1/me", headers=bearer(pair))).json()["id"])
    settings = get_settings()
    expired = tokens.issue_access(user_id, settings, datetime.now(UTC) - timedelta(hours=1))
    assert (
        await client.get("/v1/me", headers=bearer({"access_token": expired}))
    ).status_code == 401

    forged = jwt.encode(
        {"sub": str(user_id), "iss": "donut", "aud": "donut-api", "typ": "access",
         "iat": int(time.time()), "exp": int(time.time()) + 600},
        "not-our-secret-not-our-secret-not-our",
        algorithm="HS256",
    )  # fmt: skip
    assert (await client.get("/v1/me", headers=bearer({"access_token": forged}))).status_code == 401


def test_dev_secret_is_refused_outside_dev() -> None:
    settings = get_settings().model_copy(update={"env": "prod"})
    with pytest.raises(RuntimeError):
        tokens.issue_access(uuid.uuid4(), settings)


# ── web: refresh token in the HttpOnly cookie ───────────────────────────────


@pytest.fixture
async def web(client: AsyncClient) -> AsyncIterator[AsyncClient]:
    """A browser-like client on https, so Secure cookies are sent back.

    The stdlib cookie jar files a dotless host such as ``test`` under
    ``test.local``, so cookies set by hand use that domain.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="https://test") as c:
        yield c


def _cookie_attrs(res: httpx.Response) -> dict[str, str]:
    header = res.headers["set-cookie"]
    parts = [p.strip() for p in header.split(";")]
    attrs = {p.split("=", 1)[0].lower(): (p.split("=", 1)[1] if "=" in p else "") for p in parts}
    return attrs


async def _web_session(web: AsyncClient, apple: FakeApple) -> Json:
    # Web sign-in endpoints (Google, magic link) will set the cookie; until they
    # exist, start from an Apple pair and hand its refresh token to the cookie jar.
    pair = await login(web, apple)
    web.cookies.set("refresh_token", pair["refresh_token"], domain="test.local", path="/v1/auth")
    return pair


async def test_cookie_refresh_rotates_and_keeps_the_token_out_of_the_body(
    web: AsyncClient, apple: FakeApple
) -> None:
    first = await _web_session(web, apple)
    res = await web.post("/v1/auth/refresh")
    assert res.status_code == 200, res.text
    body = res.json()
    assert "refresh_token" not in body
    assert (await web.get("/v1/me", headers=bearer(body))).status_code == 200

    attrs = _cookie_attrs(res)
    new_token = attrs["refresh_token"]
    assert new_token and new_token != first["refresh_token"]
    assert {"httponly", "secure"} <= attrs.keys()
    assert attrs["samesite"].lower() == "strict"
    assert attrs["path"] == "/v1/auth"
    assert int(attrs["max-age"]) == get_settings().refresh_token_ttl_s

    # the jar now holds the rotated token, so the next refresh works too
    assert (await web.post("/v1/auth/refresh")).status_code == 200


async def test_cookie_reuse_revokes_and_clears_the_cookie(
    web: AsyncClient, apple: FakeApple
) -> None:
    first = await _web_session(web, apple)
    assert (await web.post("/v1/auth/refresh")).status_code == 200
    web.cookies.set("refresh_token", first["refresh_token"], domain="test.local", path="/v1/auth")
    res = await web.post("/v1/auth/refresh")
    assert res.status_code == 401
    attrs = _cookie_attrs(res)
    assert attrs["refresh_token"] in ("", '""')
    assert attrs["max-age"] == "0"


async def test_refresh_without_any_token_is_401(web: AsyncClient) -> None:
    res = await web.post("/v1/auth/refresh")
    assert res.status_code == 401
    assert "set-cookie" not in res.headers


async def test_oversized_cookie_is_rejected_without_a_lookup(web: AsyncClient) -> None:
    web.cookies.set("refresh_token", "x" * 1000, domain="test.local", path="/v1/auth")
    res = await web.post("/v1/auth/refresh")
    assert res.status_code == 401
    assert "x" * 50 not in res.text


async def test_body_token_still_wins_for_ios(web: AsyncClient, apple: FakeApple) -> None:
    await _web_session(web, apple)
    other = await login(web, apple, "apple-sub-2")
    res = await web.post("/v1/auth/refresh", json={"refresh_token": other["refresh_token"]})
    assert res.status_code == 200
    assert res.json()["refresh_token"]
    assert "set-cookie" not in res.headers


async def test_logout_revokes_the_family_and_clears_the_cookie(
    web: AsyncClient, apple: FakeApple
) -> None:
    first = await _web_session(web, apple)
    other_device = await login(web, apple)
    res = await web.post("/v1/auth/logout")
    assert res.status_code == 204
    assert _cookie_attrs(res)["max-age"] == "0"
    assert (await _refresh(web, first["refresh_token"])).status_code == 401
    assert (await _refresh(web, other_device["refresh_token"])).status_code == 200


async def test_logout_with_a_body_token_and_without_any_token(
    web: AsyncClient, apple: FakeApple
) -> None:
    pair = await login(web, apple)
    assert (
        await web.post("/v1/auth/logout", json={"refresh_token": pair["refresh_token"]})
    ).status_code == 204
    assert (await _refresh(web, pair["refresh_token"])).status_code == 401
    assert (await web.post("/v1/auth/logout")).status_code == 204
