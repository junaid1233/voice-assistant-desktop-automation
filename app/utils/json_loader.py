"""
JSON Loader Utility.
"""

from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def load_json(filename: str) -> dict:
    """Load JSON file from app/data."""

    file_path = BASE_DIR / "data" / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)