from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration.

    Defaults are safe for local Docker Compose. Production should override secrets via environment
    variables rather than committing them to source control.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "For My House"
    environment: str = Field(default="local", validation_alias="ENVIRONMENT")
    database_url: str = Field(
        default="postgresql+psycopg://house:house@postgres:5432/house",
        validation_alias="DATABASE_URL",
    )
    cors_origins: list[str] = Field(default=["http://localhost:3000"])
    molit_service_key: str | None = Field(default=None, validation_alias="MOLIT_SERVICE_KEY")
    naver_client_id: str | None = Field(default=None, validation_alias="NAVER_CLIENT_ID")
    naver_client_secret: str | None = Field(default=None, validation_alias="NAVER_CLIENT_SECRET")
    openai_api_key: str | None = Field(default=None, validation_alias="OPENAI_API_KEY")
    request_timeout_seconds: float = 10.0


@lru_cache
def get_settings() -> Settings:
    return Settings()
