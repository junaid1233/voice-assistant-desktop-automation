"""
Close command.
"""

from __future__ import annotations

from app.commands.base import BaseCommand
from app.services.desktop_service import DesktopService
from app.i18n import t


class CloseCommand(BaseCommand):
    """Close desktop applications."""

    def __init__(self) -> None:
        self.desktop = DesktopService()

    def can_handle(self, command: str) -> bool:
        return command.startswith("close ")

    def execute(self, command: str) -> str:
        target = command.removeprefix("close").strip().lower()

        if not target:
            return t("unknown")

        nice = {
            "chrome": "Chrome",
            "notepad": "Notepad",
            "calculator": "Calculator",
            "calc": "Calculator",
            "vscode": "VS Code",
            "vs code": "VS Code",
            "cursor": "Cursor",
        }.get(target, target.title())

        if self.desktop.close(target):
            return t("closing", target=nice)

        return t("not_running", target=nice)
