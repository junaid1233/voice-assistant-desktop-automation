"""
Application configuration.

Loads settings from the .env file.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")


class Config:
    """Application configuration."""

    ASSISTANT_NAME: str = os.getenv("ASSISTANT_NAME", "BluePilot")
    WAKE_WORD: str = os.getenv("WAKE_WORD", "bluepilot").lower()

    # Language: "en" or "ur"
    LANGUAGE: str = os.getenv("LANGUAGE", "en").lower()

    VOICE_NAME: str = os.getenv("VOICE_NAME", "en-US-GuyNeural")
    VOICE_EN: str = os.getenv("VOICE_EN", "en-US-GuyNeural")
    VOICE_UR: str = os.getenv("VOICE_UR", "ur-PK-UzmaNeural")

    STT_LANGUAGE: str = os.getenv("STT_LANGUAGE", "en-US")

    VOICE_RATE: int = int(os.getenv("VOICE_RATE", "180"))
    VOICE_VOLUME: float = float(os.getenv("VOICE_VOLUME", "1.0"))

    ENERGY_THRESHOLD: int = int(os.getenv("ENERGY_THRESHOLD", "300"))
    DYNAMIC_ENERGY: bool = os.getenv("DYNAMIC_ENERGY", "True").lower() == "true"
    PAUSE_THRESHOLD: float = float(os.getenv("PAUSE_THRESHOLD", "0.8"))
    LISTEN_TIMEOUT: int = int(os.getenv("LISTEN_TIMEOUT", "5"))
    PHRASE_TIME_LIMIT: int = int(os.getenv("PHRASE_TIME_LIMIT", "8"))

    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    NEWS_API_KEY: str | None = os.getenv("NEWS_API_KEY")
    WEATHER_API_KEY: str | None = os.getenv("WEATHER_API_KEY")

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def set_language(cls, language: str) -> None:
        """Switch assistant language (en / ur)."""
        lang = (language or "en").lower().strip()
        if lang not in {"en", "ur", "english", "urdu"}:
            lang = "en"
        if lang in {"english"}:
            lang = "en"
        if lang in {"urdu"}:
            lang = "ur"

        cls.LANGUAGE = lang
        if lang == "ur":
            cls.VOICE_NAME = cls.VOICE_UR
            cls.STT_LANGUAGE = "ur-PK"
        else:
            cls.VOICE_NAME = cls.VOICE_EN
            cls.STT_LANGUAGE = "en-US"


# Apply initial language from env
Config.set_language(Config.LANGUAGE)
