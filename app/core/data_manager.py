"""
Data Manager

Loads and caches JSON files.
"""

from __future__ import annotations

import json
from pathlib import Path


class DataManager:

    def __init__(self) -> None:

        self.base_path = (
            Path(__file__).resolve().parent.parent
            / "data"
        )

        self._cache: dict[str, dict] = {}

    def load(self, filename: str) -> dict:

        if filename in self._cache:
            return self._cache[filename]

        path = self.base_path / filename

        with open(path, "r", encoding="utf-8") as file:

            data = json.load(file)

        self._cache[filename] = data

        return data


# Global DataManager instance
data_manager = DataManager()