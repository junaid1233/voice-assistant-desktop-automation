"""
Create command.

Handles creating folders (and related create intents).
"""

from __future__ import annotations

from app.commands.base import BaseCommand
from app.services.browser_service import BrowserService
from app.services.folder_service import FolderService
from app.i18n import t


class CreateCommand(BaseCommand):
    """Create folders or open Bluexech website when asked to 'create' it."""

    def __init__(self) -> None:
        self.folders = FolderService()
        self.browser = BrowserService()

    def can_handle(self, command: str) -> bool:
        return command.startswith("create ") or command in {
            "create folder",
            "new folder",
        }

    def execute(self, command: str) -> str:
        text = command.strip().lower()

        if "bluexech" in text and ("website" in text or "site" in text or "web" in text):
            ok, name = self.browser.open("bluexech")
            if ok:
                return t("opening", target=name or "Bluexech")
            return t("opening_failed", target="Bluexech")

        if text in {"create folder", "new folder", "create new folder"}:
            ok, _path = self.folders.create("New Folder")
            return t("created_folder") if ok else t("create_failed")

        if text.startswith("create folder"):
            name = text.removeprefix("create folder").strip()
            ok, _path = self.folders.create(name or "New Folder")
            return t("created_folder") if ok else t("create_failed")

        if text.startswith("create "):
            name = text.removeprefix("create").strip()
            if name:
                ok, _path = self.folders.create(name)
                return t("created_folder") if ok else t("create_failed")

        return t("unknown")
