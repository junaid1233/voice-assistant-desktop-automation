"""
Wake word detector.
"""

from __future__ import annotations

from app.config import Config


class WakeWordDetector:
    """Detects whether the wake word is present."""

    def detect(self, text: str) -> bool:
        """
        Check if wake word exists.

        Args:
            text: Recognized speech.

        Returns:
            bool
        """

        return Config.WAKE_WORD in text.lower()