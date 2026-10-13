from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import CurrentUser
from app.auth.routing import HideInputRoute
from app.core.db import get_session
from app.users import repository
from app.users.schemas import ConsentOut, ConsentsIn, ExportOut, MeOut

router = APIRouter(prefix="/v1/me", tags=["users"], route_class=HideInputRoute)

Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=MeOut)
async def get_me(user: CurrentUser, session: Session) -> MeOut:
    return await repository.me(session, user)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(user: CurrentUser, session: Session) -> Response:
    """Delete the account and all data stored about it. This can't be undone."""
    await repository.erase(session, user.id)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/export", response_model=ExportOut)
async def export_me(user: CurrentUser, session: Session) -> ExportOut:
    return await repository.export(session, user)


@router.post("/consents", response_model=list[ConsentOut], status_code=status.HTTP_201_CREATED)
async def record_consents(
    body: ConsentsIn, user: CurrentUser, session: Session
) -> list[ConsentOut]:
    """Append consent answers (grant or withdrawal); returns the current state per type."""
    await repository.add_consents(session, user.id, body.consents)
    await session.commit()
    return await repository.current_consents(session, user.id)
