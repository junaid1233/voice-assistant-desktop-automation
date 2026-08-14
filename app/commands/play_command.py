"""
Play command.
"""

from __future__ import annotations

from app.commands.base import BaseCommand
from app.services.music_service import MusicService
from app.i18n import t


class PlayCommand(BaseCommand):
    """Handles play commands."""

    def __init__(self) -> None:
        self.music = MusicService()

    def can_handle(self, command: str) -> bool:
        return command.startswith("play ")

    def execute(self, command: str) -> str:
        query = command.removeprefix("play").strip()
        if not query:
            return t("unknown")

        if self.music.play(query):
            return t("playing", target=query)

        return t("unknown")
