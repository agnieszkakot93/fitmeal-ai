"""Column encryption for the health profile (D13, Development Plan §7.2).

AES-256-GCM with a 96-bit random nonce per value. The associated data binds each
ciphertext to its user and column, so a value copied to another row or column
fails to decrypt. The key is an application secret kept apart from the database
credentials (``DONUT_PROFILE_KEY``, base64 of 32 bytes) and has an id stored
with every row, so it can be rotated: set the new key and id, move the old key
to ``DONUT_PROFILE_OLD_KEYS`` (``{"<id>": "<base64 key>"}``) and re-encrypt
with :func:`app.profile.repository.reencrypt`. There is no default key: without
one the profile can be neither read nor written (fail closed).
"""

from __future__ import annotations

import base64
import binascii
import json
import os
import uuid
from functools import lru_cache
from typing import Any

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

NONCE_BYTES = 12


class KeyUnavailable(Exception):
    """No usable key: the profile can't be read or written."""


class DecryptionFailed(Exception):
    """A stored value didn't authenticate under its key (wrong key or tampered row)."""


class ProfileKeySettings(BaseSettings):
    """Read on their own, apart from the app settings and the database URL."""

    model_config = SettingsConfigDict(env_prefix="DONUT_PROFILE_", env_file=".env", extra="ignore")

    key: SecretStr | None = None
    key_id: str = "1"
    # retired keys by id, still needed to read rows not yet re-encrypted
    old_keys: dict[str, SecretStr] = {}


def _decode_key(value: SecretStr) -> bytes:
    try:
        raw = base64.b64decode(value.get_secret_value(), validate=True)
    except (binascii.Error, ValueError):
        raise KeyUnavailable("profile key is not valid base64") from None
    if len(raw) != 32:
        raise KeyUnavailable("profile key must be 32 bytes")
    return raw


class ProfileCipher:
    def __init__(self, key_id: str, keys: dict[str, bytes]) -> None:
        if key_id not in keys:
            raise KeyUnavailable("no key for the current key id")
        self.key_id = key_id
        self._aead = {kid: AESGCM(k) for kid, k in keys.items()}

    def __repr__(self) -> str:
        return f"ProfileCipher(key_id={self.key_id!r})"

    @staticmethod
    def _aad(user_id: uuid.UUID, column: str) -> bytes:
        return f"health_profiles:{column}:{user_id}".encode()

    def encrypt(self, user_id: uuid.UUID, column: str, value: Any) -> bytes:
        nonce = os.urandom(NONCE_BYTES)
        plaintext = json.dumps(value, separators=(",", ":")).encode()
        sealed = self._aead[self.key_id].encrypt(nonce, plaintext, self._aad(user_id, column))
        return nonce + sealed

    def decrypt(self, key_id: str, user_id: uuid.UUID, column: str, blob: bytes) -> Any:
        aead = self._aead.get(key_id)
        if aead is None:
            raise KeyUnavailable("no key for the row's key id")
        try:
            plaintext = aead.decrypt(
                blob[:NONCE_BYTES], blob[NONCE_BYTES:], self._aad(user_id, column)
            )
        except InvalidTag:
            raise DecryptionFailed("stored profile did not authenticate") from None
        return json.loads(plaintext)


def cipher_from(settings: ProfileKeySettings) -> ProfileCipher:
    if settings.key is None or not settings.key.get_secret_value():
        raise KeyUnavailable("DONUT_PROFILE_KEY is not set")
    keys = {kid: _decode_key(k) for kid, k in settings.old_keys.items()}
    keys[settings.key_id] = _decode_key(settings.key)
    return ProfileCipher(settings.key_id, keys)


@lru_cache
def get_cipher() -> ProfileCipher:
    """The process-wide cipher. Raises :class:`KeyUnavailable` until a key is configured."""
    return cipher_from(ProfileKeySettings())
