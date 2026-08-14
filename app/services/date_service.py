"""
Date service.
"""

from __future__ import annotations

from datetime import datetime


class DateService:
    """Provides current date."""

    def get_date(self) -> str:
        """
        Return current date.
        """

        current_date = datetime.now().strftime("%A, %d %B %Y")

        return f"Today is {current_date}."