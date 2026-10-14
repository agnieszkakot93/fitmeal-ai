"""Recipe imports: submit, read the preview, confirm (Development Plan §2.1, §10).

Sign-in is required throughout, and every read is filtered by the owner: another
user's import id answers 404, the same as one that doesn't exist.
"""

from __future__ import annotations

import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import CurrentUser
from app.auth.routing import HideInputRoute
from app.core.db import get_session
from app.importjobs import repository
from app.importjobs.models import ImportJob, ImportOrigin, ImportStatus, ImportType
from app.importjobs.queue import Queue, get_queue
from app.importjobs.schemas import (
    MAX_TEXT_BYTES,
    ConfirmIn,
    ConfirmOut,
    ImportIn,
    ImportOut,
    PreviewOut,
    UnansweredOut,
)
from app.imports.fetch import BlockedURL, FetchLimits, check_url
from app.recipes import repository as recipes_repo
from app.recipes.router import _summary as recipe_summary

router = APIRouter(prefix="/v1/imports", tags=["imports"], route_class=HideInputRoute)

Session = Annotated[AsyncSession, Depends(get_session)]

_NOT_FOUND = "import not found"
# the JSON envelope around the largest text, escaped
_MAX_BODY_BYTES = 2 * MAX_TEXT_BYTES + 8 * 1024


def _body_size(request: Request) -> None:
    """Refuse a declared oversize body before it is parsed.

    Caddy stops bodies over its global cap before the app reads them; a tighter
    cap for this route there is the planned control (§7.7).
    """
    declared = request.headers.get("content-length", "")
    if declared.isdigit() and int(declared) > _MAX_BODY_BYTES:
        raise HTTPException(status.HTTP_413_CONTENT_TOO_LARGE, detail="body too large")


def _out(job: ImportJob) -> ImportOut:
    return ImportOut(
        id=job.id,
        type=ImportType(job.type),
        origin=ImportOrigin(job.origin),
        status=ImportStatus(job.status),
        error=job.error,
        cached=job.cache_hit,
        created_at=job.created_at,
        expires_at=job.expires_at,
        preview=PreviewOut.model_validate(job.preview) if job.preview else None,
        recipe_id=job.recipe_id,
    )


def _blocked() -> HTTPException:
    return HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, detail="blocked_url")


@router.post(
    "",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ImportOut,
    dependencies=[Depends(_body_size)],
    responses={
        413: {"description": "Body over the size cap"},
        429: {"description": "Daily import quota reached"},
        503: {"description": "The import queue is unavailable; nothing was counted"},
    },
)
async def create_import(
    body: ImportIn,
    user: CurrentUser,
    session: Session,
    queue: Annotated[Queue, Depends(get_queue)],
) -> ImportOut:
    """Queue an import. Poll `GET /v1/imports/{id}` until it is `ready` or `failed`."""
    if body.url is not None:
        try:
            # a link we'd never fetch fails now; a shared post's URL must at least be a web URL
            check_url(body.url, FetchLimits.from_settings().blocked_domains)
        except BlockedURL:
            raise _blocked() from None
    try:
        job = await repository.create(session, user.id, body.type, body.origin, body.url, body.text)
    except repository.QuotaExceeded:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS, detail="daily import quota reached"
        ) from None
    await session.commit()
    await session.refresh(job)  # server defaults
    try:
        await queue.enqueue(job.id)
    except Exception:
        # not queued: drop the job so it doesn't use up quota
        await session.delete(job)
        await session.commit()
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, detail="import queue unavailable"
        ) from None
    return _out(job)


@router.get("/{import_id}", response_model=ImportOut, responses={404: {}})
async def get_import(import_id: uuid.UUID, user: CurrentUser, session: Session) -> ImportOut:
    job = await repository.get_owned(session, user.id, import_id)
    if job is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=_NOT_FOUND)
    return _out(job)


_CONFIRM_ERRORS: dict[int | str, dict[str, Any]] = {
    404: {},
    409: {"description": "The import is not ready, or already confirmed"},
    422: {"model": UnansweredOut, "description": "Clarifications left unanswered"},
}


@router.post(
    "/{import_id}/confirm",
    status_code=status.HTTP_201_CREATED,
    response_model=ConfirmOut,
    responses=_CONFIRM_ERRORS,
)
async def confirm_import(
    import_id: uuid.UUID, body: ConfirmIn, user: CurrentUser, session: Session
) -> ConfirmOut | JSONResponse:
    """Save the preview with the answers as the user's private recipe."""
    job = await repository.get_owned(session, user.id, import_id, lock=True)
    if job is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=_NOT_FOUND)
    if job.status != ImportStatus.READY.value:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=f"import is {job.status}")
    try:
        recipe = await repository.confirm(session, user.id, job, body)
    except repository.Unanswered as e:
        out = UnansweredOut(
            detail="clarifications unanswered", positions=e.positions, missing=e.missing
        )
        return JSONResponse(out.model_dump(mode="json"), status.HTTP_422_UNPROCESSABLE_CONTENT)
    except repository.BadAnswer as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, detail=e.detail) from None
    await session.commit()
    stored = await recipes_repo.get(session, recipe.id)
    assert stored is not None
    return ConfirmOut(import_id=job.id, recipe=recipe_summary(stored))
