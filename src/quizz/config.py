"""Application settings."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Configuration values for the application.

    Attributes:
        data_dir: Directory used for default answer file locations.
        questions_file_path: Default path of the questions YAML file.
    """

    data_dir: Path = Path("data")
    questions_file_path: Path = Path("questions.yaml")

    model_config = SettingsConfigDict(
        env_prefix="QUIZZ_",
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> AppSettings:
    """Return cached application settings.

    Returns:
        AppSettings: Parsed settings instance.
    """

    return AppSettings()
