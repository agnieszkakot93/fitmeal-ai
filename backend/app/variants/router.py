"""Saved recipe variants: read one, and swap an ingredient or say "I don't have this".

Owner only: another user's variant answers 404, like a missing one. The slot
swap and rebalance endpoints live with the plans (:mod:`app.plans.router`).
"""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import CurrentUser
from app.auth.routing import HideInputRoute
from app.core.db import get_session
from app.variants import service
from app.variants.schemas import SubstituteIn, SubstituteOut, VariantOut

router = APIRouter(prefix="/v1/variants", tags=["variants"], route_class=HideInputRoute)

Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("/{variant_id}", response_model=VariantOut, responses={404: {}})
async def get_variant(variant_id: uuid.UUID, user: CurrentUser, session: Session) -> VariantOut:
    variant = await service.owned(session, user.id, variant_id, lock=False)
    return await service.variant_out(session, variant)


@router.post(
    "/{variant_id}/substitute",
    response_model=SubstituteOut,
    responses={404: {}, 409: {"description": "No safe substitute"}},
)
async def substitute(
    variant_id: uuid.UUID, body: SubstituteIn, user: CurrentUser, session: Session
) -> SubstituteOut:
    """Apply an ingredient swap, or "I don't have this", to the user's variant.

    Returns the new nutrition, the change in plain words and, for each plan day
    cooking this variant that the change moved off target, a rebalance proposal
    (applied only through `POST /v1/plans/{id}/rebalance/apply`). Exclusions come
    from the stored profile with health-data consent, else from the body.
    """
    out = await service.substitute(session, user.id, variant_id, body)
    await session.commit()
    return out
