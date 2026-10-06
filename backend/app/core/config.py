from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DONUT_", env_file=".env", extra="ignore")

    env: str = "dev"
    database_url: str = "postgresql+asyncpg://donut:donut@localhost:5432/donut"
    redis_url: str = "redis://:donut@localhost:6379/0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
