"""
Screenshot command.
"""

from __future__ import annotations

from app.commands.base import BaseCommand
from app.services.screenshot_service import ScreenshotService
from app.i18n import t


class ScreenshotCommand(BaseCommand):
    """Handles screenshot commands."""

    KEYWORDS = (
        "screenshot",
        "take screenshot",
        "capture screen",
        "capture screenshot",
    )

    def __init__(self) -> None:
        self.service = ScreenshotService()

    def can_handle(self, command: str) -> bool:
        return command in self.KEYWORDS

    def execute(self, command: str) -> str:
        path = self.service.capture()
        return t("screenshot_ok") if path else t("screenshot_fail")
