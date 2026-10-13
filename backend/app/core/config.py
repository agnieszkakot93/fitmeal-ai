from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DONUT_", env_file=".env", extra="ignore")

    env: str = "dev"
    database_url: str = "postgresql+asyncpg://donut:donut@localhost:5432/donut"
    redis_url: str = "redis://:donut@localhost:6379/0"

    # link import limits (Development Plan §7.7)
    import_max_bytes: int = 3 * 1024 * 1024  # measured after decompression
    import_deadline_s: float = 10.0  # one deadline for the whole fetch, redirects included
    import_max_redirects: int = 3
    # our own domains; a link to them or their subdomains is never fetched
    import_blocked_domains: list[str] = []


@lru_cache
def get_settings() -> Settings:
    return Settings()
