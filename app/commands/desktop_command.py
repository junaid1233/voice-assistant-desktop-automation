"""
Desktop command.
"""

from app.commands.base import BaseCommand
from app.services.desktop_service import DesktopService


class DesktopCommand(BaseCommand):

    def __init__(self) -> None:

        self.desktop = DesktopService()

    def can_handle(self, command: str) -> bool:

        apps = (
            "vscode",
            "chrome",
            "notepad",
            "calculator",
            "paint",
            "cmd",
        )

        return (
            command.startswith("open ")
            and any(app in command for app in apps)
        )

    def execute(self, command: str) -> str:

        app = command.replace("open", "").strip()

        # User may say calculator instead of calc
        if app == "calculator":
            app = "calculator"

        if self.desktop.open(app):
            return f"Opening {app}"

        return "Application not found."