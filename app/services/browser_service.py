"""
Browser service.
"""

from __future__ import annotations

import webbrowser

from app.core.data_manager import data_manager
from app.utils.logger import logger


class BrowserService:
    """Handles browser operations."""

    DISPLAY_NAMES = {
        "google": "Google",
        "youtube": "YouTube",
        "github": "GitHub",
        "linkedin": "LinkedIn",
        "linkedin profile": "your LinkedIn profile",
        "my linkedin": "your LinkedIn profile",
        "my linkedin profile": "your LinkedIn profile",
        "facebook": "Facebook",
        "bluexech": "Bluexech",
        "bluexech website": "Bluexech",
        "portfolio": "your portfolio",
    }

    def __init__(self) -> None:
        """Initialize browser service."""

        self.websites = data_manager.load("websites.json")

        logger.info("Browser service initialized.")

    def open(self, website: str) -> tuple[bool, str | None]:
        """
        Open a website in the default browser.

        Args:
            website: Website name.

        Returns:
            tuple:
                (True, Display Name)  -> Success
                (False, None)         -> Failed
        """

        website = website.lower().strip()

        url = self.websites.get(website)

        if url is None:
            logger.warning("Unknown website: %s", website)
            return False, None

        try:
            webbrowser.open(url)

            display_name = self.DISPLAY_NAMES.get(
                website,
                website.title(),
            )

            logger.info("Opened website: %s", display_name)

            return True, display_name

        except Exception as error:
            logger.exception(
                "Failed to open website '%s': %s",
                website,
                error,
            )

            return False, None