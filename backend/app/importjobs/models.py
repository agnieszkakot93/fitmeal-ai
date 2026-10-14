"""Import jobs and the import cache (Development Plan §2.1, §7.2, §7.7).

A job row carries what the worker needs, so the Redis payload is only the job
id. The pasted text is deleted when the worker finishes, success or failure;
the preview (parsed lines and matches) is deleted on confirm or expiry.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, Text, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class ImportType(StrEnum):
    LINK = "link"
    TEXT = "text"


class ImportOrigin(StrEnum):
    PASTE = "paste"
    SHARE = "share"
    PDF = "pdf"  # text the device extracted from a PDF; the file never reaches us


class ImportStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    READY = "ready"  # preview waiting for the user's answers
    FAILED = "failed"
    CONFIRMED = "confirmed"


def _in(column: str, enum: type[StrEnum]) -> str:
    return f"{column} IN ({', '.join(f"'{e.value}'" for e in enum)})"


class ImportJob(Base):
    __tablename__ = "import_jobs"
    __table_args__ = (
        CheckConstraint(_in("type", ImportType), name="type_valid"),
        CheckConstraint(_in("origin", ImportOrigin), name="origin_valid"),
        CheckConstraint(_in("status", ImportStatus), name="status_valid"),
        CheckConstraint("type = 'text' OR origin != 'pdf'", name="pdf_is_text"),
        # the daily quota counts a user's recent jobs
        Index("ix_import_jobs_user_id_created_at", "user_id", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(Text)
    origin: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, server_default=ImportStatus.QUEUED.value)
    # the link to fetch, or a shared post's URL kept as the source reference only
    source_url: Mapped[str | None] = mapped_column(Text)
    # pasted or device-extracted text; None once the worker has run
    input_text: Mapped[str | None] = mapped_column(Text)
    cache_key: Mapped[str | None] = mapped_column(Text)
    cache_hit: Mapped[bool] = mapped_column(Boolean, server_default="false")
    # a stable reason code when failed ("no_recipe", "tdm_opt_out", ...)
    error: Mapped[str | None] = mapped_column(Text)
    # schemas.PreviewOut as JSON; None until ready and again after confirm
    preview: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    recipe_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("recipes.id", ondelete="SET NULL")
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ImportCacheEntry(Base):
    """An extracted recipe (title, lines, steps), never a user's answers.

    ``user_id`` None: a public page our server fetched, shared by everyone who
    links it. Set: a private text import, visible to that user only.
    """

    __tablename__ = "import_cache"

    key: Mapped[str] = mapped_column(Text, primary_key=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    recipe: Mapped[dict[str, Any]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
