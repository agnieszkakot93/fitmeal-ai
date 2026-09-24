"""Test setup.

Database tests run against a real PostgreSQL (``FITMEAL_TEST_DATABASE_URL``,
default: the ``fitmeal_test`` database from the dev Docker Compose). The
schema is created with the real Alembic migrations.

The files in ``fixtures/fdc`` mimic the USDA FDC CSV layout; their values are
plausible test data, not reference nutrition data.
"""

import os
from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

TEST_DB_URL = os.environ.get(
    "FITMEAL_TEST_DATABASE_URL",
    "postgresql+asyncpg://fitmeal:fitmeal@localhost:5432/fitmeal_test",
)
os.environ["FITMEAL_DATABASE_URL"] = TEST_DB_URL

BACKEND_DIR = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def migrated_db() -> Iterator[None]:
    from alembic.config import Config

    from alembic import command

    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")
    yield


@pytest.fixture
async def db_session(migrated_db: None) -> AsyncIterator[AsyncSession]:
    from sqlalchemy import text

    from app.core.db import get_sessionmaker

    async with get_sessionmaker()() as session:
        await session.execute(text("TRUNCATE food_items CASCADE"))
        await session.commit()
        yield session
