"""Handing a job to the arq worker. The payload is the import id only (§7.7)."""

from __future__ import annotations

import uuid
from typing import Protocol

from arq import ArqRedis, create_pool
from arq.connections import RedisSettings

from app.core.config import get_settings

TASK = "run_import"


class Queue(Protocol):
    async def enqueue(self, import_id: uuid.UUID) -> None: ...


class ArqQueue:
    def __init__(self) -> None:
        self._pool: ArqRedis | None = None

    async def enqueue(self, import_id: uuid.UUID) -> None:
        if self._pool is None:
            self._pool = await create_pool(redis_settings())
        # arq pickles job arguments, so nothing but the id goes in
        await self._pool.enqueue_job(TASK, str(import_id), _job_id=f"import:{import_id}")


def redis_settings() -> RedisSettings:
    return RedisSettings.from_dsn(get_settings().redis_url)


_queue = ArqQueue()


def get_queue() -> Queue:
    """FastAPI dependency; tests override it."""
    return _queue
