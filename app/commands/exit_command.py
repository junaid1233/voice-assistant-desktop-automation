"""
Exit command.
"""

from __future__ import annotations

from app.commands.base import BaseCommand
from app.i18n import t


class ExitCommand(BaseCommand):
    """Handles assistant exit commands."""

    KEYWORDS = {
        "exit",
        "exist",
        "quit",
        "stop",
        "shutdown",
        "close program",
        "close assistant",
        "goodbye",
        "bye",
        "good bye",
    }

    def can_handle(self, command: str) -> bool:
        return command.strip().lower() in self.KEYWORDS

    def execute(self, command: str) -> str:
        return t("goodbye")
