"""
Music service.
"""

from __future__ import annotations

import pywhatkit

from app.core.data_manager import data_manager
from app.utils.logger import logger


class MusicService:
    """Handles music and YouTube playback."""

    def __init__(self) -> None:

        self.songs = data_manager.load("music.json")

        logger.info("Music service initialized.")

    def play(self, query: str) -> bool:
        """
        Play a song or any YouTube content.

        Args:
            query: Song name or search query.

        Returns:
            bool
        """

        query = query.lower().strip()

        if not query:
            return False

        # Favorite lookup
        search = self.songs.get(query, query)

        logger.info("Searching YouTube: %s", search)

        try:

            pywhatkit.playonyt(search)

            logger.info("Playback started.")

            return True

        except Exception:

            logger.exception(
                "Failed to play '%s'",
                search,
            )

            return False