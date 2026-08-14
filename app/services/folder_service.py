"""
Folder service.

Creates folders on the Desktop.
"""

from __future__ import annotations

from pathlib import Path

from app.utils.logger import logger


class FolderService:
    """Create folders on the user Desktop."""

    def __init__(self) -> None:
        self.desktop = Path.home() / "Desktop"
        if not self.desktop.exists():
            # OneDrive Desktop fallback (common on Windows)
            one_drive = Path.home() / "OneDrive" / "Desktop"
            self.desktop = one_drive if one_drive.exists() else Path.home()

        logger.info("Folder service initialized (%s).", self.desktop)

    def create(self, name: str | None = None) -> tuple[bool, str]:
        """
        Create a folder on Desktop.

        Returns:
            (success, message_or_path)
        """
        folder_name = (name or "New Folder").strip() or "New Folder"
        # keep filename safe
        for ch in '<>:"/\\|?*':
            folder_name = folder_name.replace(ch, "")

        path = self.desktop / folder_name

        if path.exists():
            index = 2
            while True:
                candidate = self.desktop / f"{folder_name} {index}"
                if not candidate.exists():
                    path = candidate
                    break
                index += 1

        try:
            path.mkdir(parents=True, exist_ok=False)
            logger.info("Created folder: %s", path)
            return True, str(path)
        except Exception as error:
            logger.exception("Failed to create folder: %s", error)
            return False, str(error)
