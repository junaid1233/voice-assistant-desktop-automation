"""
Time service.
"""

from __future__ import annotations

from datetime import datetime


class TimeService:
    """Provides current time."""

    def get_time(self) -> str:
        """
        Return current time.
        """

        current_time = datetime.now().strftime("%I:%M %p")

        return f"The current time is {current_time}."