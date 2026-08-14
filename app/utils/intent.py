"""
Intent detection for reliable spoken commands (EN / Roman Urdu / Urdu).
"""

from __future__ import annotations

import re


def _has_any(text: str, words: list[str]) -> bool:
    return any(w in text for w in words)


# Desktop apps that support open + close
_CLOSEABLE_APPS = {
    "chrome": "chrome",
    "google chrome": "chrome",
    "notepad": "notepad",
    "calculator": "calculator",
    "calc": "calculator",
    "vscode": "vscode",
    "vs code": "vscode",
    "visual studio code": "vscode",
    "cursor": "cursor",
    "slack": "slack",
}


def detect_intent(raw: str) -> str | None:
    """
    Map free speech to a canonical command.

    Returns canonical command string or None.
    """
    if not raw:
        return None

    text = raw.strip()
    lower = text.lower()
    compact = re.sub(r"\s+", " ", lower)

    close_words = ["close", "band karo", "band kar", "band kar do", "kill", "terminate"]
    open_words = ["open", "kholo", "khol", "start", "launch"]
    is_close = _has_any(compact, close_words) or "بند" in text
    is_open = _has_any(compact, open_words) or "کھول" in text or "اوپن" in text

    # Close specific app BEFORE generic exit
    # e.g. "close chrome", "chrome band karo", "کرسر بند کرو"
    for key, app in _CLOSEABLE_APPS.items():
        urdu_keys = {
            "chrome": ["کروم", "گوگل کروم"],
            "notepad": ["نوٹ پیڈ", "نوٹپید"],
            "calculator": ["کیلکولیٹر"],
            "vscode": ["وی ایس کوڈ"],
            "cursor": ["کرسر"],
            "slack": ["سلیک"],
        }
        matched = key in compact or _has_any(text, urdu_keys.get(app, []))
        if matched and is_close:
            return f"close {app}"

    # Exit assistant (only when no app target)
    if _has_any(compact, ["exit", "quit", "goodbye", "good bye", "shutdown", "close assistant"]):
        return "exit"
    if compact.strip() in {"band karo", "band kar", "band kar do"}:
        return "exit"
    if text.strip() in {"بند کرو", "بند کر دو", "اللہ حافظ"}:
        return "exit"

    # LinkedIn profile
    if _has_any(compact, ["my linkedin", "linkedin profile", "mera linkedin", "meri linkedin", "linkdin profile"]):
        return "open linkedin profile"
    if _has_any(text, ["میرا لنکڈان", "میری لنکڈان", "لنکڈان پروفائل"]):
        return "open linkedin profile"
    if "linkedin" in compact or "linkdin" in compact or "لنکڈان" in text:
        if _has_any(compact, ["profile", "mera", "meri", "my"]) or "پروفائل" in text:
            return "open linkedin profile"
        if is_open:
            return "open linkedin"

    # Cursor open
    if ("cursor" in compact or "کرسر" in text) and not is_close:
        return "open cursor"

    # Bluexech / website
    if _has_any(compact, ["bluexech", "blue xech", "website"]) or _has_any(text, ["بلو", "ویب سائٹ", "ویبسایٹ"]):
        if _has_any(compact, ["create", "make", "banao", "build"]) or "بنا" in text:
            return "create bluexech website"
        if is_open or True:
            return "open bluexech"

    # Folder
    if "folder" in compact or "foler" in compact or "فولڈر" in text:
        if _has_any(compact, ["create", "make", "new", "banao", "bana"]) or "بنا" in text or "نیا" in text:
            return "create folder"

    # Other apps / sites open
    app_map = {
        "chrome": "open chrome",
        "notepad": "open notepad",
        "calculator": "open calculator",
        "calc": "open calculator",
        "vscode": "open vscode",
        "vs code": "open vscode",
        "youtube": "open youtube",
        "google": "open google",
        "github": "open github",
        "gmail": "open gmail",
        "facebook": "open facebook",
        "chatgpt": "open chatgpt",
        "slack": "open slack",
        "reddit": "open reddit",
        "portfolio": "open portfolio",
    }
    for key, cmd in app_map.items():
        if key in compact and not is_close:
            return cmd

    # Screenshot
    if _has_any(compact, ["screenshot", "screen shot", "capture screen"]) or "اسکرین شاٹ" in text:
        return "screenshot"

    # Time / date
    if _has_any(compact, ["time", "kitne bajay", "o'clock"]) or "وقت" in text:
        return "time"
    if _has_any(compact, ["date", "today", "aaj ki date"]) or "تاریخ" in text:
        return "date"

    # Play music
    if compact.startswith("play ") or compact.startswith("gaana ") or "چلاو" in text or "گاانا" in text:
        song = compact.replace("play ", "").replace("gaana ", "").strip()
        if song:
            return f"play {song}"

    return None
