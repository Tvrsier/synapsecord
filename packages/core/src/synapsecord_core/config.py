from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_ignore_empty=True,
    )

    synapsecord_env: Literal["development", "test", "production"] = "development"
    synapsecord_log_level: str = "INFO"

    discord_bot_token: str | None = None
    discord_guild_id: int | None = None

    postgres_host: str
    postgres_port: int = 5432
    postgres_db: str
    postgres_user: str
    postgres_password: str

    database_url: str

    profiler_poll_interval_seconds: int = 5

    riot_api_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
