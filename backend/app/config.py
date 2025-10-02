"""Application configuration settings."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Literal, Optional

import tomllib
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SlackSettings(BaseModel):
    signing_secret: str | None = Field(default=None, alias="SLACK_SIGNING_SECRET")
    bot_token: str | None = Field(default=None, alias="SLACK_BOT_TOKEN")

    @property
    def enabled(self) -> bool:
        return bool(self.signing_secret and self.bot_token)


CONFIG_DIR = Path(__file__).resolve().parent
SETTINGS_PATH = CONFIG_DIR / "settings.toml"
EXAMPLE_SETTINGS_PATH = CONFIG_DIR / "settings.example.toml"


def _load_settings_from_toml() -> dict[str, Any]:
    """Load settings overrides from a TOML file when available."""

    target = SETTINGS_PATH if SETTINGS_PATH.exists() else None
    if target is None and EXAMPLE_SETTINGS_PATH.exists():
        target = EXAMPLE_SETTINGS_PATH
    if target is None:
        return {}
    with target.open("rb") as handle:
        data = tomllib.load(handle)
    if not isinstance(data, dict):
        return {}
    return data


class Settings(BaseSettings):
    """Application settings loaded from environment variables and TOML files."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", populate_by_name=True
    )

    database_url: str = Field(
        default="postgresql+psycopg://demo:demo@localhost:5432/agents",
        alias="DATABASE_URL",
    )
    qdrant_url: str = Field(default="http://localhost:6333", alias="QDRANT_URL")
    llm_provider: Literal["openai", "anthropic", "fake"] = Field(
        default="fake", alias="LLM_PROVIDER"
    )
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, alias="ANTHROPIC_API_KEY")
    timezone: str = Field(default="Europe/Madrid", alias="TIMEZONE")
    slack: SlackSettings = Field(default_factory=SlackSettings)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        """Inject TOML-based configuration before environment overrides."""

        def toml_settings(*_: Any) -> dict[str, Any]:
            return _load_settings_from_toml()

        return (
            init_settings,
            env_settings,
            dotenv_settings,
            toml_settings,
            file_secret_settings,
        )


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()


__all__ = ["Settings", "SlackSettings", "get_settings"]
