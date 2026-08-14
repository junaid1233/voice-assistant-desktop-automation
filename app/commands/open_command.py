"""
Open command.

Handles opening websites and desktop applications.
"""

from __future__ import annotations

from app.commands.base import BaseCommand
from app.services.browser_service import BrowserService
from app.services.desktop_service import DesktopService
from app.i18n import t


class OpenCommand(BaseCommand):
    """Open websites or desktop applications."""

    def __init__(self) -> None:
        self.browser = BrowserService()
        self.desktop = DesktopService()

    def can_handle(self, command: str) -> bool:
        return command.startswith("open ")

    def execute(self, command: str) -> str:
        target = command.removeprefix("open").strip().lower()

        if not target:
            return t("unknown")

        linkedin_aliases = {
            "my linkedin",
            "my linkedin profile",
            "linkedin profile",
            "linkedin profiles",
            "linkdin",
            "my linkdin",
            "my linkdin profile",
            "linkdin profile",
        }
        if target in linkedin_aliases:
            target = "linkedin profile"

        if target in {"bluexech website", "bluexech site", "blue xech"}:
            target = "bluexech"

        display = target

        if self.desktop.open(target):
            nice = {
                "cursor": "Cursor",
                "chrome": "Chrome",
                "notepad": "Notepad",
                "calculator": "Calculator",
                "vscode": "VS Code",
                "slack": "Slack",
            }.get(target, target.title())
            return t("opening", target=nice)

        ok, name = self.browser.open(target)
        if ok:
            return t("opening", target=name or display)

        return t("opening_failed", target=display)
