"""Application settings, loaded from environment / .env file."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Default to a local SQLite file so the API runs with zero setup in dev.
    # In production set DATABASE_URL to a Postgres DSN, e.g.
    #   postgresql+asyncpg://user:pass@host:5432/gridlet
    database_url: str = "sqlite+aiosqlite:///./gridlet.db"

    jwt_secret: str = "dev-secret-change-me-in-production-please-32+chars"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

    # Origins allowed to call the API (the Svelte front).
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://penotdev-code.github.io",
    ]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
