"""Login and refresh-token rotation with reuse detection."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import tokens
from app.auth.apple import AppleIdentity
from app.auth.models import RefreshToken
from app.auth.schemas import TokenPair
from app.core.config import Settings
from app.users.models import User


class InvalidRefreshToken(Exception):
    pass


async def upsert_user(session: AsyncSession, identity: AppleIdentity) -> uuid.UUID:
    stmt = (
        insert(User)
        .values(apple_sub=identity.sub, email_relay=identity.email_relay)
        .on_conflict_do_nothing(index_elements=[User.apple_sub])
    )
    await session.execute(stmt)
    user = (await session.scalars(select(User).where(User.apple_sub == identity.sub))).one()
    if identity.email_relay is not None and user.email_relay != identity.email_relay:
        user.email_relay = identity.email_relay
    return user.id


async def issue_pair(
    session: AsyncSession,
    user_id: uuid.UUID,
    settings: Settings,
    family_id: uuid.UUID | None = None,
) -> TokenPair:
    now = datetime.now(UTC)
    refresh = tokens.new_refresh_token()
    session.add(
        RefreshToken(
            user_id=user_id,
            family_id=family_id or uuid.uuid4(),
            token_hash=tokens.hash_refresh_token(refresh),
            expires_at=now + timedelta(seconds=settings.refresh_token_ttl_s),
        )
    )
    return TokenPair(
        access_token=tokens.issue_access(user_id, settings, now),
        refresh_token=refresh,
        expires_in=settings.access_token_ttl_s,
        refresh_expires_in=settings.refresh_token_ttl_s,
    )


async def rotate(session: AsyncSession, presented: str, settings: Settings) -> TokenPair:
    """Spend ``presented`` and issue the next pair in its family; commits.

    The spend is one conditional UPDATE, so two concurrent requests with the
    same token can't both succeed. Presenting a spent or revoked token is
    treated as theft: the whole family is revoked and the caller must sign in
    with Apple again.
    """
    token_hash = tokens.hash_refresh_token(presented)
    now = datetime.now(UTC)
    spent = (
        await session.execute(
            update(RefreshToken)
            .where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.used_at.is_(None),
                RefreshToken.revoked_at.is_(None),
                RefreshToken.expires_at > now,
            )
            .values(used_at=now)
            .returning(RefreshToken.user_id, RefreshToken.family_id)
        )
    ).one_or_none()
    if spent is None:
        old = (
            await session.scalars(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
        ).one_or_none()
        if old is not None and (old.used_at is not None or old.revoked_at is not None):
            await revoke_family(session, old.family_id, now)
            await session.commit()
        raise InvalidRefreshToken
    pair = await issue_pair(session, spent.user_id, settings, spent.family_id)
    await session.commit()
    return pair


async def revoke(session: AsyncSession, presented: str) -> None:
    """Sign out: revoke ``presented`` and the rest of its family; commits."""
    token_hash = tokens.hash_refresh_token(presented)
    family_id = await session.scalar(
        select(RefreshToken.family_id).where(RefreshToken.token_hash == token_hash)
    )
    if family_id is not None:
        await revoke_family(session, family_id, datetime.now(UTC))
        await session.commit()


async def revoke_family(session: AsyncSession, family_id: uuid.UUID, now: datetime) -> None:
    await session.execute(
        update(RefreshToken)
        .where(RefreshToken.family_id == family_id, RefreshToken.revoked_at.is_(None))
        .values(revoked_at=now)
    )
