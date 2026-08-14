"""
Date command.
"""

from __future__ import annotations

from app.commands.base import BaseCommand
from app.services.date_service import DateService


class DateCommand(BaseCommand):

    def __init__(self) -> None:

        self.service = DateService()

    def can_handle(self, command: str) -> bool:

        return "date" in command or "today" in command

    def execute(self, command: str) -> str:

        return self.service.get_date()