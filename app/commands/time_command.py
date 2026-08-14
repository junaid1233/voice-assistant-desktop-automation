"""
Time command.
"""

from __future__ import annotations

from app.commands.base import BaseCommand
from app.services.time_service import TimeService


class TimeCommand(BaseCommand):

    def __init__(self) -> None:

        self.service = TimeService()

    def can_handle(self, command: str) -> bool:

        return "time" in command

    def execute(self, command: str) -> str:

        return self.service.get_time()