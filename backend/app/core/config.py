from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FinTrack"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"

    mongodb_uri: str = "mongodb://127.0.0.1:27017"
    mongodb_database: str = "fintrack"

    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
