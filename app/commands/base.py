"""
Base command.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """Abstract base class for all commands."""

    @abstractmethod
    def can_handle(self, command: str) -> bool:
        """
        Check whether this command can handle the input.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self, command: str) -> str:
        """
        Execute the command.
        """
        raise NotImplementedError