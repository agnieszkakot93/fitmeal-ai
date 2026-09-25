from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="FITMEAL_", env_file=".env", extra="ignore")

    env: str = "dev"
    database_url: str = "postgresql+asyncpg://fitmeal:fitmeal@localhost:5432/fitmeal"
    redis_url: str = "redis://:fitmeal@localhost:6379/0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
