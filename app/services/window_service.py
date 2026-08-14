"""
Window service.

Handles desktop window operations.
"""

from __future__ import annotations

import pygetwindow as gw

from app.utils.logger import logger


class WindowService:
    """Handles desktop windows."""

    def __init__(self) -> None:

        logger.info("Window service initialized.")

    def _find_window(self, title: str):

        """
        Find a window by partial title.

        Returns:
            Window | None
        """

        title = title.lower().strip()

        try:

            for window in gw.getAllWindows():

                if not window.title:
                    continue

                if title in window.title.lower():

                    return window

        except Exception:

            logger.exception(
                "Failed to enumerate windows."
            )

        return None

    def focus(self, title: str) -> bool:
        """
        Bring window to the foreground.
        """

        window = self._find_window(title)

        if not window:

            logger.warning(
                "Window not found: %s",
                title,
            )

            return False

        try:

            if window.isMinimized:
                window.restore()

            window.activate()

            logger.info(
                "Focused window: %s",
                window.title,
            )

            return True

        except Exception:

            logger.exception(
                "Failed to focus '%s'",
                title,
            )

            return False

    def minimize(self, title: str) -> bool:
        """
        Minimize a window.
        """

        window = self._find_window(title)

        if not window:

            logger.warning(
                "Window not found: %s",
                title,
            )

            return False

        try:

            window.minimize()

            logger.info(
                "Minimized window: %s",
                window.title,
            )

            return True

        except Exception:

            logger.exception(
                "Failed to minimize '%s'",
                title,
            )

            return False

    def maximize(self, title: str) -> bool:
        """
        Maximize a window.
        """

        window = self._find_window(title)

        if not window:

            logger.warning(
                "Window not found: %s",
                title,
            )

            return False

        try:

            if window.isMinimized:
                window.restore()

            window.maximize()

            logger.info(
                "Maximized window: %s",
                window.title,
            )

            return True

        except Exception:

            logger.exception(
                "Failed to maximize '%s'",
                title,
            )

            return False

    def restore(self, title: str) -> bool:
        """
        Restore a window.
        """

        window = self._find_window(title)

        if not window:

            logger.warning(
                "Window not found: %s",
                title,
            )

            return False

        try:

            window.restore()

            window.activate()

            logger.info(
                "Restored window: %s",
                window.title,
            )

            return True

        except Exception:

            logger.exception(
                "Failed to restore '%s'",
                title,
            )

            return False