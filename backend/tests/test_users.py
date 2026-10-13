"""Users API: /v1/me, consents, export and erasure."""

import asyncio
import uuid
from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import delete, func, select, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from app.auth.models import RefreshToken
from app.core.db import get_sessionmaker
from app.recipes.models import Recipe, RecipeSource, RecipeVariant
from app.users.models import ConsentRecord, User
from tests.conftest import BACKEND_DIR, TEST_DB_URL
from tests.test_auth import FakeApple, apple, apple_key, bearer, client, login

__all__ = ["apple", "apple_key", "client"]  # fixtures shared with test_auth

Json = dict[str, Any]


async def _me(c: AsyncClient, pair: Json) -> Json:
    res = await c.get("/v1/me", headers=bearer(pair))
    assert res.status_code == 200
    body: Json = res.json()
    return body


async def _consent(c: AsyncClient, pair: Json, *consents: Json) -> Any:
    res = await c.post("/v1/me/consents", json={"consents": list(consents)}, headers=bearer(pair))
    assert res.status_code == 201, res.text
    return res.json()


HEALTH = {"type": "health_data", "version": "2026-10-01", "granted": True}
AGE = {"type": "age_18_plus", "version": "1", "granted": True}


async def test_me(client: AsyncClient, apple: FakeApple) -> None:
    pair = await login(client, apple)
    me = await _me(client, pair)
    assert set(me) == {"id", "created_at", "email_relay", "consents"}
    assert me["consents"] == []


async def test_consents_are_appended(client: AsyncClient, apple: FakeApple) -> None:
    pair = await login(client, apple)
    state = await _consent(client, pair, HEALTH, AGE)
    assert {c["type"] for c in state} == {"health_data", "age_18_plus"}

    # withdrawal is a new record; the current state follows the latest one
    state = await _consent(client, pair, {**HEALTH, "granted": False})
    assert {c["type"]: c["granted"] for c in state} == {"health_data": False, "age_18_plus": True}
    me = await _me(client, pair)
    assert {c["type"]: c["granted"] for c in me["consents"]}["health_data"] is False

    async with get_sessionmaker()() as session:
        rows = (await session.scalars(select(ConsentRecord))).all()
    assert len(rows) == 3


async def test_consent_records_cannot_be_updated(client: AsyncClient, apple: FakeApple) -> None:
    pair = await login(client, apple)
    await _consent(client, pair, HEALTH)
    async with get_sessionmaker()() as session:
        with pytest.raises(DBAPIError, match="append-only"):
            await session.execute(text("UPDATE consent_records SET granted = false"))
        await session.rollback()


@pytest.mark.parametrize(
    "body",
    [
        {"consents": [{**HEALTH, "type": "marketing"}]},
        {"consents": [{**HEALTH, "version": "has spaces"}]},
        {"consents": [{**HEALTH, "recorded_at": "2020-01-01T00:00:00Z"}]},
        {"consents": []},
    ],
)
async def test_bad_consents_are_rejected(client: AsyncClient, apple: FakeApple, body: Json) -> None:
    pair = await login(client, apple)
    res = await client.post("/v1/me/consents", json=body, headers=bearer(pair))
    assert res.status_code == 422
    assert all("input" not in e for e in res.json()["detail"])


async def test_consents_need_auth(client: AsyncClient) -> None:
    res = await client.post("/v1/me/consents", json={"consents": [HEALTH]})
    assert res.status_code == 401


async def _private_recipe(owner: uuid.UUID, title: str) -> None:
    async with get_sessionmaker()() as session:
        source = RecipeSource(type="text", content_hash=title)
        session.add(source)
        await session.flush()
        recipe = Recipe(source_id=source.id, owner_user_id=owner, title_en=title, servings=2)
        session.add(recipe)
        await session.flush()
        session.add(RecipeVariant(base_recipe_id=recipe.id, user_id=owner, label=f"{title} v"))
        await session.commit()


async def _cleanup(*titles: str) -> None:
    """Drop the recipes ``_private_recipe`` made (their content_hash is the title)."""
    async with get_sessionmaker()() as session:
        sources = select(RecipeSource.id).where(RecipeSource.content_hash.in_(titles))
        await session.execute(delete(Recipe).where(Recipe.source_id.in_(sources)))
        await session.execute(delete(RecipeSource).where(RecipeSource.content_hash.in_(titles)))
        await session.commit()


async def test_export_contains_everything_stored(client: AsyncClient, apple: FakeApple) -> None:
    pair = await login(client, apple)
    other = await login(client, apple, "someone-else")
    me = await _me(client, pair)
    other_id = uuid.UUID((await _me(client, other))["id"])
    await _consent(client, pair, HEALTH)
    await _consent(client, pair, {**HEALTH, "granted": False})
    await _private_recipe(uuid.UUID(me["id"]), "my soup")
    await _private_recipe(other_id, "their soup")
    try:
        res = await client.get("/v1/me/export", headers=bearer(pair))
        assert res.status_code == 200
        body = res.json()
    finally:
        await _cleanup("my soup", "their soup")

    assert body["user"]["id"] == me["id"]
    assert [c["granted"] for c in body["consent_history"]] == [True, False]
    assert len(body["sessions"]) == 1
    assert "token_hash" not in res.text
    assert pair["refresh_token"] not in res.text
    assert [r["title_en"] for r in body["private_recipes"]] == ["my soup"]
    assert body["private_recipes"][0]["source"]["type"] == "text"
    assert [v["label"] for v in body["recipe_variants"]] == ["my soup v"]


async def test_delete_removes_everything(client: AsyncClient, apple: FakeApple) -> None:
    pair = await login(client, apple)
    await login(client, apple)  # a second session
    other = await login(client, apple, "someone-else")
    user_id = uuid.UUID((await _me(client, pair))["id"])
    other_id = uuid.UUID((await _me(client, other))["id"])
    await _consent(client, pair, HEALTH, AGE)
    await _consent(client, other, HEALTH)
    await _private_recipe(user_id, "mine")
    await _private_recipe(other_id, "theirs")
    try:
        res = await client.delete("/v1/me", headers=bearer(pair))
        assert res.status_code == 204

        async with get_sessionmaker()() as session:

            async def count(model: Any, *where: Any) -> int:
                stmt = select(func.count()).select_from(model).where(*where)
                return int(await session.scalar(stmt) or 0)

            assert await count(User, User.id == user_id) == 0
            assert await count(RefreshToken, RefreshToken.user_id == user_id) == 0
            assert await count(ConsentRecord, ConsentRecord.user_id == user_id) == 0
            assert await count(Recipe, Recipe.owner_user_id == user_id) == 0
            assert await count(RecipeVariant, RecipeVariant.user_id == user_id) == 0
            assert await count(RecipeSource, RecipeSource.content_hash == "mine") == 0
            # nobody else's data goes with it
            assert await count(User, User.id == other_id) == 1
            assert await count(ConsentRecord, ConsentRecord.user_id == other_id) == 1
            assert await count(Recipe, Recipe.owner_user_id == other_id) == 1
            assert await count(RecipeVariant, RecipeVariant.user_id == other_id) == 1
    finally:
        await _cleanup("mine", "theirs")

    # the old tokens are dead
    assert (await client.get("/v1/me", headers=bearer(pair))).status_code == 401
    res = await client.post("/v1/auth/refresh", json={"refresh_token": pair["refresh_token"]})
    assert res.status_code == 401
    # signing in again starts a new, empty account
    again = await login(client, apple)
    me = await _me(client, again)
    assert me["id"] != str(user_id)
    assert me["consents"] == []


async def test_delete_needs_auth(client: AsyncClient) -> None:
    assert (await client.delete("/v1/me")).status_code == 401
    assert (await client.get("/v1/me/export")).status_code == 401


def test_migration_down_and_up(migrated_db: None) -> None:
    from alembic.config import Config

    from alembic import command

    async def tables() -> set[str]:
        engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)
        async with engine.connect() as conn:
            rows = await conn.execute(
                text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
            )
            names = {r[0] for r in rows}
        await engine.dispose()
        return names

    ours = {"users", "refresh_tokens", "consent_records"}
    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    command.downgrade(cfg, "0005")
    try:
        assert not ours & asyncio.run(tables())
    finally:
        command.upgrade(cfg, "head")
    assert ours <= asyncio.run(tables())
