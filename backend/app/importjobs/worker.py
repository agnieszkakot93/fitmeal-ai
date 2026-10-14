"""The arq worker: ``arq app.importjobs.worker.WorkerSettings``.

``run_import`` reads everything it needs from the job row; tests call it
directly with a ``ctx`` that swaps in a fake resolver and HTTP transport.
Logs carry the import id, type, size, duration and outcome, never content.
"""

from __future__ import annotations

import logging
import time
import uuid
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import Any, ClassVar

from arq import cron, func
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.db import get_sessionmaker
from app.importjobs import cache, extract, preview, repository
from app.importjobs.config import get_import_settings
from app.importjobs.models import ImportJob, ImportStatus, ImportType
from app.importjobs.queue import TASK, redis_settings
from app.imports.fetch import FetchError, system_resolver
from app.imports.page import PageUnusable, read_recipe_page

# arq logs job arguments at INFO (§7.7); ours are ids, but keep it quiet anyway
logging.getLogger("arq").setLevel(logging.WARNING)
log = logging.getLogger(__name__)


class NoRecipe(Exception):
    pass


def _sessionmaker(ctx: dict[str, Any]) -> async_sessionmaker[AsyncSession]:
    maker: async_sessionmaker[AsyncSession] = ctx.get("sessionmaker") or get_sessionmaker()
    return maker


async def _draft(
    session: AsyncSession, job: ImportJob, ctx: dict[str, Any]
) -> tuple[extract.Draft, bool]:
    """The extracted recipe and whether it came from the cache."""
    private = job.type == ImportType.TEXT.value
    if private:
        assert job.input_text is not None
        key = cache.text_key(job.user_id, job.input_text)
    else:
        assert job.source_url is not None
        key = cache.link_key(job.source_url)
    job.cache_key = key
    owner = job.user_id if private else None
    cached = await cache.get(session, key, owner)
    if cached is not None:
        return cached, True

    if private:
        assert job.input_text is not None
        draft = extract.from_text(job.input_text)
    else:
        assert job.source_url is not None
        page = await read_recipe_page(
            job.source_url,
            limits=ctx.get("fetch_limits"),
            resolver=ctx.get("resolver", system_resolver),
            transport=ctx.get("transport"),
        )
        draft = extract.from_page(page)
    if not draft.ingredients:
        raise NoRecipe
    ttl = timedelta(days=get_import_settings().import_cache_ttl_days)
    # a shared entry holds parsed facts only, never the site's own wording (§7.3)
    entry = draft if private else replace(draft, instructions=[])
    await cache.put(session, key, owner, entry, ttl)
    return draft, False


async def _fail(session: AsyncSession, import_id: uuid.UUID, reason: str) -> None:
    await session.rollback()
    await session.execute(
        update(ImportJob)
        .where(ImportJob.id == import_id)
        .values(
            status=ImportStatus.FAILED.value,
            error=reason,
            input_text=None,
            finished_at=datetime.now(UTC),
        )
    )


async def run_import(ctx: dict[str, Any], import_id: str) -> None:
    job_id = uuid.UUID(import_id)
    async with _sessionmaker(ctx)() as session:
        job = await repository.claim(session, job_id, retry=ctx.get("job_try", 1) > 1)
        if job is None:
            return
        started = time.monotonic()
        job_type = job.type
        size = len(job.input_text.encode()) if job.input_text else 0
        outcome = "ready"
        try:
            draft, hit = await _draft(session, job, ctx)
            result = await preview.build(session, draft, job.source_url)
            job.preview = result.model_dump(mode="json")
            job.cache_hit = hit
            job.status = ImportStatus.READY.value
            job.input_text = None  # the raw text goes as soon as parsing ends (§7.2)
            job.finished_at = datetime.now(UTC)
            await session.commit()
            if hit:
                outcome = "ready_cached"
        except (PageUnusable, FetchError) as e:
            outcome = e.reason
        except NoRecipe:
            outcome = "no_recipe"
        except Exception as e:
            # the message may quote content; log the type only
            outcome = "internal_error"
            log.error("import %s raised %s", job_id, type(e).__name__)
        if outcome not in ("ready", "ready_cached"):
            await _fail(session, job_id, outcome)
            await session.commit()
        log.info(
            "import %s type=%s size=%d duration_ms=%d outcome=%s",
            job_id,
            job_type,
            size,
            (time.monotonic() - started) * 1000,
            outcome,
        )


async def purge_expired(ctx: dict[str, Any]) -> None:
    async with _sessionmaker(ctx)() as session:
        stale = await repository.fail_stale(session)
        jobs = await repository.purge_expired(session)
        entries = await cache.purge_expired(session)
        await session.commit()
    log.info(
        "failed %d stale imports, purged %d expired imports and %d cache entries",
        stale,
        jobs,
        entries,
    )


class WorkerSettings:
    functions: ClassVar = [func(run_import, name=TASK)]
    # every 10 minutes: a timed-out or lost job's text doesn't wait for expiry
    cron_jobs: ClassVar = [cron(purge_expired, minute=set(range(7, 60, 10)))]
    redis_settings = redis_settings()
    keep_result = 0  # no job results (or arguments) left in Redis (§7.7)
    job_timeout = 60
    max_jobs = 4
