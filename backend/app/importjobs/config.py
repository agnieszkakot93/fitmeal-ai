"""Import job limits. Separate from ``app.core.config`` so the feature owns its settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ImportJobSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DONUT_", env_file=".env", extra="ignore")

    # hard abuse cap per user over the last 24 hours, counted on submission (§2.4, §7.7);
    # the per-plan monthly quotas arrive with entitlements (S8)
    import_daily_quota: int = 20
    # unconfirmed previews and their source lines are deleted after this (§7.7)
    import_preview_ttl_days: int = 7
    import_cache_ttl_days: int = 30


@lru_cache
def get_import_settings() -> ImportJobSettings:
    return ImportJobSettings()
