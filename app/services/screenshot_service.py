"""
Screenshot service.

Captures and saves screenshots.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pyautogui

from app.utils.logger import logger


class ScreenshotService:
    """Handles screenshots."""

    def __init__(self) -> None:

        self.directory = Path("screenshots")
        self.directory.mkdir(exist_ok=True)

        logger.info("Screenshot service initialized.")

    def capture(self) -> str | None:
        """
        Capture the current screen.

        Returns:
            Saved file path or None.
        """

        try:

            filename = (
                f"screenshot_"
                f"{datetime.now():%Y-%m-%d_%H-%M-%S}.png"
            )

            filepath = self.directory / filename

            image = pyautogui.screenshot()

            image.save(filepath)

            logger.info(
                "Screenshot saved: %s",
                filepath,
            )

            return str(filepath)

        except Exception:

            logger.exception(
                "Failed to capture screenshot."
            )

            return None