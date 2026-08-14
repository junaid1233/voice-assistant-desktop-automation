"""
Wake Word Detection.
"""

from app.config import Config


class WakeWordDetector:
    """Detects the assistant wake word."""

    def __init__(self) -> None:
        self.wake_word = Config.WAKE_WORD.lower()

    def detect(self, text: str | None) -> bool:
        """
        Return True if wake word is present.
        """

        if not text:
            return False

        return self.wake_word in text.lower()

    def remove(self, text: str) -> str:
        """
        Remove wake word from command.
        """

        return (
            text.lower()
            .replace(self.wake_word, "")
            .strip()
        )