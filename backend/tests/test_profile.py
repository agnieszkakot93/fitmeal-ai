"""The stored health profile (D13): encryption, the consent gate, export, deletion, plans."""

from __future__ import annotations

import asyncio
import base64
import logging
import os
import uuid
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select, text

from app.core.db import get_sessionmaker
from app.plans.models import MealPlan
from app.profile import cli, crypto, repository
from app.profile.crypto import (
    DecryptionFailed,
    KeyUnavailable,
    ProfileKeySettings,
    cipher_from,
    get_cipher,
)
from app.profile.models import HealthProfile
from app.profile.schemas import HealthProfileIn
from tests.test_auth import FakeApple, apple, apple_key, bearer, client, login
from tests.test_plans import BODY, PROFILE, api, snapshot_catalog

__all__ = ["api", "apple", "apple_key", "client", "snapshot_catalog"]  # shared fixtures

Json = dict[str, Any]

HEALTH = {"type": "health_data", "version": "2026-10-01", "granted": True}
WITHDRAW = {**HEALTH, "granted": False}

# distinctive values, so a leak in the database or the logs is easy to spot
STORED: Json = {
    **PROFILE,
    "daily_kcal": 2137,
    "protein_min_g": 123,
    "exclusions": [
        {"category": "peanuts", "severity": "allergy"},
        {"category": "other", "severity": "dislike", "term": "zzcorianderzz"},
    ],
    "body": {
        "age": 41,
        "sex": "female",
        "weight_kg": 77.7,
        "height_cm": 171.3,
        "activity_level": "moderate",
    },
}
SECRETS = ("2137", "77.7", "171.3", "peanuts", "zzcorianderzz", "moderate", "oven", "blender")


def _key() -> str:
    return base64.b64encode(os.urandom(32)).decode()


@pytest.fixture(autouse=True)
def profile_key(monkeypatch: pytest.MonkeyPatch) -> Iterator[str]:
    key = _key()
    monkeypatch.setenv("DONUT_PROFILE_KEY", key)
    monkeypatch.setenv("DONUT_PROFILE_KEY_ID", "k1")
    monkeypatch.delenv("DONUT_PROFILE_OLD_KEYS", raising=False)
    get_cipher.cache_clear()
    yield key
    get_cipher.cache_clear()


async def _consent(c: AsyncClient, pair: Json, *consents: Json) -> None:
    res = await c.post("/v1/me/consents", json={"consents": list(consents)}, headers=bearer(pair))
    assert res.status_code == 201, res.text


async def _put(c: AsyncClient, pair: Json, body: Json = STORED) -> Any:
    return await c.put("/v1/me/profile", json=body, headers=bearer(pair))


async def _user_id(c: AsyncClient, pair: Json) -> uuid.UUID:
    return uuid.UUID((await c.get("/v1/me", headers=bearer(pair))).json()["id"])


async def _rows() -> int:
    async with get_sessionmaker()() as session:
        return int(await session.scalar(select(func.count()).select_from(HealthProfile)) or 0)


async def _raw_rows() -> str:
    """Every stored profile as Postgres sees it, bytea in hex and as text."""
    async with get_sessionmaker()() as session:
        rows = await session.scalars(
            text(
                "SELECT row_to_json(h)::text || encode("
                "targets || body_data || exclusions || preferences, 'escape') "
                "FROM health_profiles h"
            )
        )
        return " ".join(rows)


# ── round trip and storage ──────────────────────────────────────────────────


async def test_round_trip(client: AsyncClient, apple: FakeApple) -> None:
    pair = await login(client, apple)
    await _consent(client, pair, HEALTH)
    assert (await client.get("/v1/me/profile", headers=bearer(pair))).status_code == 404

    res = await _put(client, pair)
    assert res.status_code == 200, res.text
    saved = res.json()
    assert saved["version"] == 1
    expected = {
        **STORED,
        "exclusions": [{"term": None, "relaxed": False, **e} for e in STORED["exclusions"]],
    }
    assert {k: v for k, v in saved.items() if k not in ("version", "updated_at")} == expected

    got = (await client.get("/v1/me/profile", headers=bearer(pair))).json()
    assert got == saved

    # a save replaces the whole profile and bumps the version
    res = await _put(client, pair, {**STORED, "daily_kcal": 1800, "body": None})
    assert res.json()["version"] == 2
    assert res.json()["daily_kcal"] == 1800 and res.json()["body"] is None
    assert await _rows() == 1


async def test_only_ciphertext_is_stored(client: AsyncClient, apple: FakeApple) -> None:
    pair = await login(client, apple)
    await _consent(client, pair, HEALTH)
    assert (await _put(client, pair)).status_code == 200

    stored = await _raw_rows()
    for value in (*SECRETS, "daily_kcal", "category", "weight_kg", "female"):
        assert value not in stored
    async with get_sessionmaker()() as session:
        row = (await session.scalars(select(HealthProfile))).one()
    assert row.key_id == "k1"
    # a fresh nonce per value: the same profile never encrypts the same way twice
    first = row.targets
    await _put(client, pair)
    async with get_sessionmaker()() as session:
        again = (await session.scalars(select(HealthProfile))).one()
    assert again.targets != first


async def test_a_value_moved_to_another_row_fails(client: AsyncClient, apple: FakeApple) -> None:
    mine = await login(client, apple)
    theirs = await login(client, apple, "someone-else")
    for pair in (mine, theirs):
        await _consent(client, pair, HEALTH)
        assert (await _put(client, pair)).status_code == 200
    mine_id, theirs_id = await _user_id(client, mine), await _user_id(client, theirs)
    async with get_sessionmaker()() as session:
        await session.execute(
            text(
                "UPDATE health_profiles SET exclusions = "
                "(SELECT exclusions FROM health_profiles WHERE user_id = :src) "
                "WHERE user_id = :dst"
            ),
            {"src": theirs_id, "dst": mine_id},
        )
        await session.commit()
    res = await client.get("/v1/me/profile", headers=bearer(mine))
    assert res.status_code == 503
    assert res.json()["detail"] == "health_profile_unavailable"


async def test_an_older_value_spliced_in_fails(client: AsyncClient, apple: FakeApple) -> None:
    """An old ``exclusions`` (say from a backup, before an allergy was added) won't authenticate."""
    pair = await login(client, apple)
    await _consent(client, pair, HEALTH)
    assert (await _put(client, pair, {**STORED, "exclusions": []})).status_code == 200
    async with get_sessionmaker()() as session:
        old = (await session.scalars(select(HealthProfile))).one().exclusions
    assert (await _put(client, pair)).status_code == 200
    async with get_sessionmaker()() as session:
        await session.execute(text("UPDATE health_profiles SET exclusions = :old"), {"old": old})
        await session.commit()
    res = await client.get("/v1/me/profile", headers=bearer(pair))
    assert res.status_code == 503
    assert "peanuts" not in res.text


@pytest.mark.parametrize(
    "change",
    [
        {"daily_kcal": 1100},
        {"body": {"age": 16}},
        {"body": {"weight_kg": 500}},
        {"body": {"diagnosis": "x"}},
        {"meals": [{**m, "kcal_share": 0.2} for m in PROFILE["meals"]]},
        {"exclusions": [{"category": "milk", "severity": "x"}]},
        {"notes": "anything"},
    ],
)
async def test_bad_profile_is_rejected_without_echo(
    client: AsyncClient, apple: FakeApple, change: Json
) -> None:
    pair = await login(client, apple)
    await _consent(client, pair, HEALTH)
    res = await _put(client, pair, {**STORED, **change})
    assert res.status_code == 422
    assert all("input" not in e for e in res.json()["detail"])
    assert "zzcorianderzz" not in res.text
    assert await _rows() == 0


async def test_needs_auth(client: AsyncClient) -> None:
    assert (await client.get("/v1/me/profile")).status_code == 401
    assert (await client.put("/v1/me/profile", json=STORED)).status_code == 401


# ── consent ─────────────────────────────────────────────────────────────────


async def test_consent_is_required(client: AsyncClient, apple: FakeApple) -> None:
    pair = await login(client, apple)
    for res in (
        await client.get("/v1/me/profile", headers=bearer(pair)),
        await _put(client, pair),
    ):
        assert res.status_code == 403
        assert res.json()["detail"] == "health_data_consent_required"
    assert await _rows() == 0

    # other consents don't count
    await _consent(client, pair, {"type": "terms_of_use", "version": "1", "granted": True})
    assert (await _put(client, pair)).status_code == 403


async def test_withdrawal_deletes_the_profile(client: AsyncClient, apple: FakeApple) -> None:
    pair = await login(client, apple)
    other = await login(client, apple, "someone-else")
    for p in (pair, other):
        await _consent(client, p, HEALTH)
        assert (await _put(client, p)).status_code == 200
    assert await _rows() == 2

    await _consent(client, pair, WITHDRAW)
    assert await _rows() == 1  # only the other user's remains
    for res in (
        await client.get("/v1/me/profile", headers=bearer(pair)),
        await _put(client, pair),
    ):
        assert res.status_code == 403
    assert await _rows() == 1

    # granting again starts empty
    await _consent(client, pair, HEALTH)
    assert (await client.get("/v1/me/profile", headers=bearer(pair))).status_code == 404


async def test_one_answer_per_consent_type(client: AsyncClient, apple: FakeApple) -> None:
    """A grant and a withdrawal in one batch would share a timestamp: which one is current?"""
    pair = await login(client, apple)
    res = await client.post(
        "/v1/me/consents", json={"consents": [HEALTH, WITHDRAW]}, headers=bearer(pair)
    )
    assert res.status_code == 422
    assert (await _put(client, pair)).status_code == 403


async def test_withdrawal_waits_for_a_save_in_flight(client: AsyncClient, apple: FakeApple) -> None:
    """A save holding the user lock commits first; the withdrawal then deletes what it wrote."""
    pair = await login(client, apple)
    await _consent(client, pair, HEALTH)
    user_id = await _user_id(client, pair)
    async with get_sessionmaker()() as saving:
        await repository.lock_user(saving, user_id)
        assert await repository.has_health_consent(saving, user_id)
        body = HealthProfileIn.model_validate(STORED)
        await repository.put(saving, get_cipher(), user_id, body)
        withdrawal = asyncio.create_task(_consent(client, pair, WITHDRAW))
        await asyncio.sleep(0.5)
        assert not withdrawal.done()  # blocked on the lock
        await saving.commit()
    await asyncio.wait_for(withdrawal, 10)
    assert await _rows() == 0


async def test_save_after_a_withdrawal_in_flight_is_refused(
    client: AsyncClient, apple: FakeApple
) -> None:
    pair = await login(client, apple)
    await _consent(client, pair, HEALTH)
    user_id = await _user_id(client, pair)
    async with get_sessionmaker()() as withdrawing:
        await repository.lock_user(withdrawing, user_id)
        await withdrawing.execute(
            text(
                "INSERT INTO consent_records (user_id, type, version, granted) "
                "VALUES (:u, 'health_data', '2026-10-01', false)"
            ),
            {"u": user_id},
        )
        save = asyncio.create_task(_put(client, pair))
        await asyncio.sleep(0.5)
        assert not save.done()  # blocked on the lock
        await withdrawing.commit()
    res = await asyncio.wait_for(save, 10)
    assert res.status_code == 403
    assert await _rows() == 0


# ── keys ────────────────────────────────────────────────────────────────────


async def test_missing_key_fails_closed(
    client: AsyncClient, apple: FakeApple, monkeypatch: pytest.MonkeyPatch
) -> None:
    pair = await login(client, apple)
    await _consent(client, pair, HEALTH)
    assert (await _put(client, pair)).status_code == 200

    monkeypatch.delenv("DONUT_PROFILE_KEY")
    get_cipher.cache_clear()
    for res in (
        await client.get("/v1/me/profile", headers=bearer(pair)),
        await _put(client, pair, {**STORED, "daily_kcal": 1900}),
        await client.get("/v1/me/export", headers=bearer(pair)),
    ):
        assert res.status_code == 503
        assert res.json()["detail"] == "health_profile_unavailable"
    # the failed save wrote nothing: the stored row is still the first one
    async with get_sessionmaker()() as session:
        row = (await session.scalars(select(HealthProfile))).one()
    assert row.version == 1


async def test_wrong_key_fails_closed(
    client: AsyncClient, apple: FakeApple, monkeypatch: pytest.MonkeyPatch
) -> None:
    pair = await login(client, apple)
    await _consent(client, pair, HEALTH)
    assert (await _put(client, pair)).status_code == 200

    # same key id, different key: authentication fails, nothing is returned
    monkeypatch.setenv("DONUT_PROFILE_KEY", _key())
    get_cipher.cache_clear()
    res = await client.get("/v1/me/profile", headers=bearer(pair))
    assert res.status_code == 503
    assert "2137" not in res.text


@pytest.mark.parametrize("key", ["", "not base64!", base64.b64encode(b"short").decode()])
def test_bad_key_settings_are_refused(key: str) -> None:
    with pytest.raises(KeyUnavailable):
        cipher_from(ProfileKeySettings(key=key or None))


def test_cipher_rejects_tampering() -> None:
    cipher = cipher_from(ProfileKeySettings(key=_key(), key_id="k1"))
    user = uuid.uuid4()
    blob = cipher.encrypt(user, "targets", 3, {"daily_kcal": 2000})
    assert cipher.decrypt("k1", user, "targets", 3, blob) == {"daily_kcal": 2000}
    flipped = blob[:-1] + bytes([blob[-1] ^ 1])
    for args in (
        ("k1", user, "targets", 3, flipped),
        ("k1", uuid.uuid4(), "targets", 3, blob),  # another user
        ("k1", user, "exclusions", 3, blob),  # another column
        ("k1", user, "targets", 4, blob),  # another save
    ):
        with pytest.raises(DecryptionFailed):
            cipher.decrypt(*args)
    with pytest.raises(KeyUnavailable):
        cipher.decrypt("k0", user, "targets", 3, blob)
    assert "k1" in repr(cipher) and "key=" not in repr(cipher)


async def test_key_rotation(
    client: AsyncClient,
    apple: FakeApple,
    monkeypatch: pytest.MonkeyPatch,
    profile_key: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    pair = await login(client, apple)
    other = await login(client, apple, "someone-else")
    for p in (pair, other):
        await _consent(client, p, HEALTH)
    saved = (await _put(client, pair)).json()
    await _put(client, other)
    # a row under a key nobody has any more: reported, and it doesn't stall the rest
    async with get_sessionmaker()() as session:
        await session.execute(
            text("UPDATE health_profiles SET key_id = 'lost' WHERE user_id = :u"),
            {"u": await _user_id(client, other)},
        )
        await session.commit()

    # a new current key, the old one kept for reading
    monkeypatch.setenv("DONUT_PROFILE_KEY", _key())
    monkeypatch.setenv("DONUT_PROFILE_KEY_ID", "k2")
    monkeypatch.setenv("DONUT_PROFILE_OLD_KEYS", f'{{"k1": "{profile_key}"}}')
    get_cipher.cache_clear()
    assert (await client.get("/v1/me/profile", headers=bearer(pair))).json() == saved

    assert await cli.rotate(batch=1) == 1  # the lost row is left
    out = capsys.readouterr()
    assert "re-encrypted 1 profile(s)" in out.out
    assert str(await _user_id(client, other)) in out.err
    for value in SECRETS:
        assert value not in out.out + out.err
    async with get_sessionmaker()() as session:
        keys = sorted((await session.scalars(select(HealthProfile.key_id))).all())
    assert keys == ["k2", "lost"]

    # the old key is no longer needed; content, version and update time are unchanged
    monkeypatch.delenv("DONUT_PROFILE_OLD_KEYS")
    get_cipher.cache_clear()
    assert (await client.get("/v1/me/profile", headers=bearer(pair))).json() == saved


async def test_rotation_without_a_key_does_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DONUT_PROFILE_KEY")
    get_cipher.cache_clear()
    assert await cli.rotate() == 1


def test_key_from_a_secret_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Docker secrets: the key can live in a file instead of the environment."""
    monkeypatch.delenv("DONUT_PROFILE_KEY")
    (tmp_path / "donut_profile_key").write_text(_key() + "\n")
    settings = ProfileKeySettings(_secrets_dir=tmp_path)
    assert cipher_from(settings).key_id == "k1"
    monkeypatch.setattr(crypto, "SECRETS_DIR", tmp_path)
    get_cipher.cache_clear()
    assert get_cipher().key_id == "k1"


# ── logs ────────────────────────────────────────────────────────────────────


async def test_profile_never_reaches_the_logs(
    api: AsyncClient, apple: FakeApple, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.DEBUG)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)  # statements and parameters
    try:
        pair = await login(api, apple)
        await _consent(api, pair, HEALTH)
        await _put(api, pair)
        await _put(api, pair, {**STORED, "daily_kcal": 1100})  # rejected
        await api.get("/v1/me/profile", headers=bearer(pair))
        await api.post("/v1/plans", json={"days": 3}, headers=bearer(pair))
        await api.get("/v1/me/export", headers=bearer(pair))
        await _consent(api, pair, WITHDRAW)
    finally:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    assert caplog.records  # the capture works
    logged = caplog.text + " ".join(str(r.args) for r in caplog.records)
    for value in SECRETS:
        assert value not in logged


# ── export and deletion ─────────────────────────────────────────────────────


async def test_export_includes_the_profile(client: AsyncClient, apple: FakeApple) -> None:
    pair = await login(client, apple)
    res = await client.get("/v1/me/export", headers=bearer(pair))
    assert res.json()["health_profile"] is None

    await _consent(client, pair, HEALTH)
    saved = (await _put(client, pair)).json()
    res = await client.get("/v1/me/export", headers=bearer(pair))
    assert res.status_code == 200
    assert res.json()["health_profile"] == saved


async def test_account_deletion_deletes_the_profile(client: AsyncClient, apple: FakeApple) -> None:
    pair = await login(client, apple)
    other = await login(client, apple, "someone-else")
    for p in (pair, other):
        await _consent(client, p, HEALTH)
        assert (await _put(client, p)).status_code == 200
    user_id = await _user_id(client, pair)

    assert (await client.delete("/v1/me", headers=bearer(pair))).status_code == 204
    async with get_sessionmaker()() as session:
        mine = await session.scalar(
            select(func.count()).select_from(HealthProfile).where(HealthProfile.user_id == user_id)
        )
    assert mine == 0
    assert await _rows() == 1


# ── plans ───────────────────────────────────────────────────────────────────


async def _plan(c: AsyncClient, pair: Json, body: Json) -> Any:
    return await c.post("/v1/plans", json=body, headers=bearer(pair))


async def test_plan_uses_the_stored_profile(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    await _consent(api, pair, HEALTH)
    stored = {**STORED, "daily_kcal": 2200, "protein_min_g": 110, "exclusions": []}
    assert (await _put(api, pair, stored)).status_code == 200

    # no snapshot needed
    res = await _plan(api, pair, {"days": 3, "prep_days": 2})
    assert res.status_code == 201, res.text
    assert res.json()["targets"] == {"daily_kcal": 2200, "protein_min_g": 110}
    # a snapshot is ignored while the stored profile applies
    res = await _plan(api, pair, BODY)
    assert res.json()["targets"] == {"daily_kcal": 2200, "protein_min_g": 110}


async def test_plan_falls_back_to_the_snapshot(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    snapshot_targets = {"daily_kcal": PROFILE["daily_kcal"], "protein_min_g": 120}

    # no stored profile
    await _consent(api, pair, HEALTH)
    res = await _plan(api, pair, BODY)
    assert res.status_code == 201, res.text
    assert res.json()["targets"] == snapshot_targets

    # a stored profile but the consent withdrawn (which also deletes it)
    assert (await _put(api, pair, {**STORED, "exclusions": []})).status_code == 200
    await _consent(api, pair, WITHDRAW)
    res = await _plan(api, pair, BODY)
    assert res.json()["targets"] == snapshot_targets

    # neither: a validation error in the documented shape, nothing saved
    before = await _count_plans()
    res = await _plan(api, pair, {"days": 3})
    assert res.status_code == 422
    assert res.json()["detail"][0]["loc"] == ["body", "profile"]
    assert await _count_plans() == before


async def test_plan_without_consent_ignores_a_leftover_row(
    api: AsyncClient, apple: FakeApple
) -> None:
    """Belt and braces: even if a row survived, no consent means it isn't read."""
    pair = await login(api, apple)
    await _consent(api, pair, HEALTH)
    assert (
        await _put(api, pair, {**STORED, "daily_kcal": 2200, "exclusions": []})
    ).status_code == 200
    async with get_sessionmaker()() as session:
        # a withdrawal recorded behind the API's back, so the row stays
        await session.execute(
            text(
                "INSERT INTO consent_records (user_id, type, version, granted) "
                "VALUES (:u, 'health_data', '2026-10-01', false)"
            ),
            {"u": await _user_id(api, pair)},
        )
        await session.commit()
    res = await _plan(api, pair, BODY)
    assert res.json()["targets"]["daily_kcal"] == PROFILE["daily_kcal"]


async def test_profile_saved_under_older_rules(api: AsyncClient, apple: FakeApple) -> None:
    """A rule tightened after a save: the profile stays readable, but isn't planned from."""
    pair = await login(api, apple)
    await _consent(api, pair, HEALTH)
    user_id = await _user_id(api, pair)
    # what an older, looser schema would have accepted
    old = HealthProfileIn.model_construct(
        **{**HealthProfileIn.model_validate(STORED).__dict__, "daily_kcal": 1000.0}
    )
    async with get_sessionmaker()() as session:
        await repository.lock_user(session, user_id)
        await repository.put(session, get_cipher(), user_id, old)
        await session.commit()

    got = await api.get("/v1/me/profile", headers=bearer(pair))
    assert got.status_code == 200 and got.json()["daily_kcal"] == 1000
    export = await api.get("/v1/me/export", headers=bearer(pair))
    assert export.json()["health_profile"]["daily_kcal"] == 1000
    # the stored profile (with its allergies) still wins over a snapshot
    res = await _plan(api, pair, BODY)
    assert res.status_code == 422
    assert res.json()["detail"][0]["type"] == "outdated"
    # saving it again under the current rules fixes it
    assert (await _put(api, pair, {**STORED, "exclusions": []})).status_code == 200
    assert (await _plan(api, pair, BODY)).status_code == 201


async def _count_plans() -> int:
    async with get_sessionmaker()() as session:
        return int(await session.scalar(select(func.count()).select_from(MealPlan)) or 0)
