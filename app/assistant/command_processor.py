"""
Command Processor.

Processes spoken commands and routes them
to the appropriate command handler.
"""

from __future__ import annotations

from app.commands.router import CommandRouter
from app.utils.command_parser import CommandParser
from app.utils.intent import detect_intent
from app.utils.logger import logger
from app.i18n import t


class CommandProcessor:
    """Processes user commands."""

    def __init__(self) -> None:
        self.router = CommandRouter()

    def process(self, command: str) -> str | None:
        """
        Returns response string, or None to stay silent.
        """
        if not command or not command.strip():
            return None

        raw = command.strip()
        logger.info("Heard raw: %s", raw)

        # 1) Intent engine (most reliable for voice)
        intent = detect_intent(raw)
        if intent:
            logger.info("Intent matched: %s", intent)
            return self.router.handle(intent)

        # 2) Classic normalize path
        normalized = CommandParser.normalize(raw)
        logger.info("Normalized command: %s", normalized)

        if not normalized:
            return None

        # Try intent again on normalized text
        intent = detect_intent(normalized)
        if intent:
            logger.info("Intent matched after normalize: %s", intent)
            return self.router.handle(intent)

        response = self.router.handle(normalized)
        logger.info("Response: %s", response)
        return response
