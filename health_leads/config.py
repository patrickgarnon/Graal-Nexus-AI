"""Configuration du microservice Graal Health Leads (variables d'environnement)."""
from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="GRAAL_HEALTH_",
    )

    environment: str = Field(default="development")

    brevo_api_key: str = Field(default="")
    brevo_sender_email: str = Field(default="no-reply@sanojagroup.com")
    brevo_sender_name: str = Field(default="Jouvence du Graal")

    sheets_webhook_url: str = Field(default="")
    sheets_webhook_secret: str = Field(default="")

    rate_limit_per_minute: int = Field(default=5, ge=1)
    allowed_origins: str = Field(default="*")

    @property
    def allowed_origins_list(self) -> list[str]:
        if self.allowed_origins == "*":
            return ["*"]
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
