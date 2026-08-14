"""
Desktop service.

Handles desktop applications.
"""

from __future__ import annotations

import subprocess

import psutil

from app.core.data_manager import data_manager
from app.utils.logger import logger


class DesktopService:
    """Desktop application service."""

    def __init__(self) -> None:
        self.apps = data_manager.load("apps.json")
        logger.info("Desktop service initialized.")

    def _process_names(self, app: dict) -> list[str]:
        raw = app.get("process", [])
        if isinstance(raw, str):
            return [raw.lower()]
        return [str(p).lower() for p in raw]

    def open(self, app_name: str) -> bool:
        app_name = app_name.lower().strip()
        app = self.apps.get(app_name)

        if not app:
            logger.warning("Unknown application: %s", app_name)
            return False

        try:
            target = app["open"]
            if isinstance(target, str) and (target.lower().endswith(".exe") or "\\" in target or "/" in target):
                subprocess.Popen([target])
            else:
                subprocess.Popen(target, shell=True)

            logger.info("Opened application: %s", app_name)
            return True
        except Exception:
            logger.exception("Failed to open %s", app_name)
            return False

    def close(self, app_name: str) -> bool:
        app_name = app_name.lower().strip()
        aliases = {
            "vs code": "vscode",
            "visual studio code": "vscode",
            "calc": "calculator",
            "google chrome": "chrome",
        }
        app_name = aliases.get(app_name, app_name)

        app = self.apps.get(app_name)
        if not app:
            logger.warning("Unknown application: %s", app_name)
            return False

        targets = set(self._process_names(app))
        closed = False

        for process in psutil.process_iter(["pid", "name"]):
            try:
                name = process.info["name"]
                if not name:
                    continue
                if name.lower() in targets:
                    process.terminate()
                    try:
                        process.wait(timeout=3)
                    except psutil.TimeoutExpired:
                        process.kill()
                    closed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if closed:
            logger.info("Closed application: %s", app_name)
        else:
            logger.warning("%s is not running.", app_name)

        return closed
