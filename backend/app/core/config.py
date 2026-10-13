from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# signs dev and test tokens only; app.auth.tokens refuses it in any other env
DEV_JWT_SECRET = "dev-only-insecure-jwt-secret-do-not-use-in-prod"


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

    # auth (Development Plan §7.7). The default secret only works when env is dev or test.
    jwt_secret: SecretStr = SecretStr(DEV_JWT_SECRET)
    access_token_ttl_s: int = 15 * 60
    refresh_token_ttl_s: int = 30 * 24 * 3600
    # Sign in with Apple: the bundle/Services IDs our identity tokens are issued for
    # (`aud`). Empty until the bundle ID is set (RENAME_PLAN phase 3); login fails closed.
    apple_client_ids: list[str] = []
    apple_jwks_url: str = "https://appleid.apple.com/auth/keys"


@lru_cache
def get_settings() -> Settings:
    return Settings()
