"""
Window command.
"""

from __future__ import annotations

from app.commands.base import BaseCommand
from app.services.window_service import WindowService


class WindowCommand(BaseCommand):
    """Handles window management commands."""

    ACTIONS = (
        "focus",
        "minimize",
        "maximize",
        "restore",
    )

    def __init__(self) -> None:

        self.window = WindowService()

    def can_handle(self, command: str) -> bool:

        return any(
            command.startswith(action + " ")
            for action in self.ACTIONS
        )

    def execute(self, command: str) -> str:

        action, _, target = command.partition(" ")

        target = target.strip()

        if not target:
            return f"Which window should I {action}?"

        match action:

            case "focus":
                success = self.window.focus(target)

            case "minimize":
                success = self.window.minimize(target)

            case "maximize":
                success = self.window.maximize(target)

            case "restore":
                success = self.window.restore(target)

            case _:
                return "Unknown window command."

        if success:
            return f"{action.capitalize()}d {target}."

        return f"I couldn't {action} {target}."