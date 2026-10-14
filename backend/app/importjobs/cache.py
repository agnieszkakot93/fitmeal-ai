"""Import cache keys and storage (Development Plan §2.4, §7.7 "Import cache").

- A link's key comes from the URL the user submitted, normalised, never from
  the page (a hostile page could claim a popular URL with a canonical tag).
  Link entries are shared: they hold only what our server fetched itself.
- A text import's key is ``HMAC(server secret, user id, content hash)`` and its
  entry belongs to that user. A shared post's URL never keys text.
- Keys include ``PIPELINE_VERSION``; entries expire.
"""

from __future__ import annotations

import hashlib
import hmac
import unicodedata
import uuid
from datetime import UTC, datetime, timedelta
from functools import lru_cache
from urllib.parse import urlsplit, urlunsplit

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.importjobs.extract import Draft
from app.importjobs.models import ImportCacheEntry

# bump when extraction changes; the LLM step adds its prompt, model and schema versions
PIPELINE_VERSION = "deterministic-1"
_DEFAULT_PORTS = {"http": 80, "https": 443}


def normalise_url(url: str) -> str:
    """Lower-case scheme and host, drop the default port, fragment and ``utm_*``.

    Path and query keep their case and order: ``?p=123`` often names the recipe.
    """
    parts = urlsplit(url.strip())
    scheme = parts.scheme.lower()
    host = (parts.hostname or "").rstrip(".")
    netloc = host if parts.port in (None, _DEFAULT_PORTS.get(scheme)) else f"{host}:{parts.port}"
    query = "&".join(
        p for p in parts.query.split("&") if p and not p.split("=", 1)[0].lower().startswith("utm_")
    )
    return urlunsplit((scheme, netloc, parts.path or "/", query, ""))


def normalise_text(text: str) -> str:
    lines = (" ".join(line.split()) for line in unicodedata.normalize("NFC", text).splitlines())
    return "\n".join(line for line in lines if line)


@lru_cache
def _secret() -> bytes:
    # a key of its own, derived from the server secret, so cache keys can't be
    # turned into tokens or the other way round
    root = get_settings().jwt_secret.get_secret_value().encode()
    return hmac.new(root, b"donut/import-cache/v1", hashlib.sha256).digest()


def link_key(url: str) -> str:
    digest = hashlib.sha256(f"{PIPELINE_VERSION}\n{normalise_url(url)}".encode()).hexdigest()
    return f"link:{digest}"


def text_key(user_id: uuid.UUID, text: str) -> str:
    content = hashlib.sha256(normalise_text(text).encode()).hexdigest()
    message = f"{PIPELINE_VERSION}\n{user_id}\n{content}".encode()
    return "text:" + hmac.new(_secret(), message, hashlib.sha256).hexdigest()


async def get(session: AsyncSession, key: str, user_id: uuid.UUID | None) -> Draft | None:
    """A live entry; ``user_id`` None reads only shared entries."""
    owner = (
        ImportCacheEntry.user_id.is_(None)
        if user_id is None
        else ImportCacheEntry.user_id == user_id
    )
    entry = await session.scalar(
        select(ImportCacheEntry).where(
            ImportCacheEntry.key == key, owner, ImportCacheEntry.expires_at > datetime.now(UTC)
        )
    )
    return Draft.from_json(entry.recipe) if entry else None


async def put(
    session: AsyncSession, key: str, user_id: uuid.UUID | None, draft: Draft, ttl: timedelta
) -> None:
    now = datetime.now(UTC)
    values = {"recipe": draft.to_json(), "created_at": now, "expires_at": now + ttl}
    stmt = insert(ImportCacheEntry).values(key=key, user_id=user_id, **values)
    await session.execute(stmt.on_conflict_do_update(index_elements=["key"], set_=values))


async def purge_expired(session: AsyncSession) -> int:
    result = await session.execute(
        delete(ImportCacheEntry).where(ImportCacheEntry.expires_at <= datetime.now(UTC))
    )
    return int(getattr(result, "rowcount", 0) or 0)
