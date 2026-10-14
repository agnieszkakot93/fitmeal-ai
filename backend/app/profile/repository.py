"""Reading and writing the encrypted profile, and the health-data consent gate.

Nothing here logs: profile values, decrypted or not, never reach a log line.
"""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import delete, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.profile.crypto import ProfileCipher
from app.profile.models import ENCRYPTED, HealthProfile
from app.profile.schemas import HealthProfileIn, HealthProfileOut
from app.users.models import ConsentRecord, ConsentType, User


async def has_health_consent(session: AsyncSession, user_id: uuid.UUID) -> bool:
    """Whether the latest ``health_data`` answer is a grant (Art. 9(2)(a))."""
    latest = await session.scalar(
        select(ConsentRecord.granted)
        .where(ConsentRecord.user_id == user_id, ConsentRecord.type == ConsentType.HEALTH_DATA)
        .order_by(ConsentRecord.recorded_at.desc(), ConsentRecord.id.desc())
        .limit(1)
    )
    return bool(latest)


async def lock_user(session: AsyncSession, user_id: uuid.UUID) -> None:
    """Serialize profile writes with consent changes, so a withdrawal can't race a save."""
    await session.execute(select(User.id).where(User.id == user_id).with_for_update())


def _split(profile: HealthProfileIn) -> dict[str, Any]:
    data = profile.model_dump(mode="json")
    return {
        "targets": {"daily_kcal": data["daily_kcal"], "protein_min_g": data["protein_min_g"]},
        "body_data": data["body"],
        "exclusions": data["exclusions"],
        "preferences": {
            "meals": data["meals"],
            "max_minutes": data["max_minutes"],
            "equipment": data["equipment"],
        },
    }


def _seal(
    cipher: ProfileCipher, user_id: uuid.UUID, version: int, fields: dict[str, Any]
) -> dict[str, Any]:
    sealed = {c: cipher.encrypt(user_id, c, version, v) for c, v in fields.items()}
    return sealed | {"key_id": cipher.key_id}


def _open(cipher: ProfileCipher, row: HealthProfile) -> dict[str, Any]:
    def read(column: str) -> Any:
        return cipher.decrypt(row.key_id, row.user_id, column, row.version, getattr(row, column))

    return {
        **read("targets"),
        **read("preferences"),
        "exclusions": read("exclusions"),
        "body": read("body_data"),
    }


async def exists(session: AsyncSession, user_id: uuid.UUID) -> bool:
    found = await session.scalar(
        select(HealthProfile.user_id).where(HealthProfile.user_id == user_id)
    )
    return found is not None


async def get(
    session: AsyncSession, cipher: ProfileCipher, user_id: uuid.UUID
) -> HealthProfileOut | None:
    row = await session.get(HealthProfile, user_id, populate_existing=True)
    if row is None:
        return None
    return HealthProfileOut.model_validate(
        {**_open(cipher, row), "version": row.version, "updated_at": row.updated_at}
    )


async def put(
    session: AsyncSession, cipher: ProfileCipher, user_id: uuid.UUID, profile: HealthProfileIn
) -> None:
    """Insert or replace the whole profile. The caller holds :func:`lock_user`.

    The new version is part of every column's associated data, so columns from
    different saves can't be mixed.
    """
    current = await session.scalar(
        select(HealthProfile.version).where(HealthProfile.user_id == user_id)
    )
    version = (current or 0) + 1
    values = _seal(cipher, user_id, version, _split(profile)) | {"version": version}
    stmt = insert(HealthProfile).values(user_id=user_id, **values)
    await session.execute(
        stmt.on_conflict_do_update(
            index_elements=[HealthProfile.user_id], set_={**values, "updated_at": func.now()}
        )
    )


async def delete_profile(session: AsyncSession, user_id: uuid.UUID) -> None:
    """Hard delete: no tombstone, no copy kept."""
    await session.execute(delete(HealthProfile).where(HealthProfile.user_id == user_id))


async def reencrypt(session: AsyncSession, cipher: ProfileCipher, batch: int = 500) -> int:
    """Re-encrypt rows still under a retired key with the current one; returns how many.

    The rows are locked one batch at a time, so the caller commits between calls
    until it returns 0.
    """
    rows = (
        await session.scalars(
            select(HealthProfile)
            .where(HealthProfile.key_id != cipher.key_id)
            .limit(batch)
            .with_for_update(skip_locked=True)
        )
    ).all()
    for row in rows:
        fields = {
            c: cipher.decrypt(row.key_id, row.user_id, c, row.version, getattr(row, c))
            for c in ENCRYPTED
        }
        for column, value in _seal(cipher, row.user_id, row.version, fields).items():
            setattr(row, column, value)
    await session.flush()
    return len(rows)
