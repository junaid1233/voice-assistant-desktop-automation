"""
Command parser.

Normalizes spoken commands.
"""

from __future__ import annotations

from app.config import Config


class CommandParser:
    """Normalizes voice commands."""

    # Applied first on raw text (before filler removal)
    PHRASE_ALIASES = {
        "open my linkedin profile": "open linkedin profile",
        "open my linkedin": "open linkedin profile",
        "open linkedin profile": "open linkedin profile",
        "open my linkdin profile": "open linkedin profile",
        "open my linkdin": "open linkedin profile",
        "open linkdin profile": "open linkedin profile",
        "open linkdin": "open linkedin",
        "create bluexech website": "create bluexech website",
        "make bluexech website": "create bluexech website",
        "build bluexech website": "create bluexech website",
        "bluexech website banao": "create bluexech website",
        "open bluexech website": "open bluexech",
        "open bluexech site": "open bluexech",
        "open bluexech": "open bluexech",
        "create new folder": "create folder",
        "make new folder": "create folder",
        "make a new folder": "create folder",
        "new folder create": "create folder",
        "create a new folder": "create folder",
        "open cursor ide": "open cursor",
        "open the cursor": "open cursor",
        # Roman Urdu
        "cursor kholo": "open cursor",
        "cursor open karo": "open cursor",
        "folder banao": "create folder",
        "naya folder banao": "create folder",
        "new folder banao": "create folder",
        "linkedin kholo": "open linkedin profile",
        "mera linkedin kholo": "open linkedin profile",
        "meri linkedin profile kholo": "open linkedin profile",
        "website kholo": "open bluexech",
        "bluexech kholo": "open bluexech",
        "band karo": "exit",
        "band kar do": "exit",
        "exit karo": "exit",
        "chrome band karo": "close chrome",
        "close the chrome": "close chrome",
        "notepad band karo": "close notepad",
        "calculator band karo": "close calculator",
        "cursor band karo": "close cursor",
        "vscode band karo": "close vscode",
        "close chrome": "close chrome",
        "close notepad": "close notepad",
        "close calculator": "close calculator",
        "close cursor": "close cursor",
        "close vscode": "close vscode",
        "close vs code": "close vscode",
        "slack band karo": "close slack",
        "close slack": "close slack",
        "slack kholo": "open slack",
        "open slack desktop": "open slack",
        "time kya hua": "time",
        "kitne bajay": "time",
        "aaj ki date": "date",
        # Urdu script
        "کرسر کھولو": "open cursor",
        "کرسر اوپن کرو": "open cursor",
        "کرسر بند کرو": "close cursor",
        "کروم بند کرو": "close chrome",
        "نوٹ پیڈ بند کرو": "close notepad",
        "کیلکولیٹر بند کرو": "close calculator",
        "نیا فولڈر بناؤ": "create folder",
        "فولڈر بناؤ": "create folder",
        "میرا لنکڈان کھولو": "open linkedin profile",
        "میری لنکڈان پروفائل کھولو": "open linkedin profile",
        "لنکڈان کھولو": "open linkedin profile",
        "ویب سائٹ کھولو": "open bluexech",
        "بلو ایکس کھولو": "open bluexech",
        "بند کرو": "exit",
        "بند کر دو": "exit",
        "وقت کیا ہوا": "time",
        "آج کی تاریخ": "date",
    }

    GREETINGS = {
        "hey",
        "hello",
        "hi",
        "ok",
        "okay",
    }

    FILLER_WORDS = {
        "the",
        "a",
        "an",
        "please",
        "could",
        "would",
        "can",
        "you",
        "me",
        "to",
    }

    ALIASES = {
        "launch": "open",
        "start": "open",
        "run": "open",
        "terminate": "close",
        "kill": "close",
        "end": "close",
        "exist": "exit",
        "exits": "exit",
        "bring": "focus",
        "activate": "focus",
        "switch": "focus",
        "shrink": "minimize",
        "fullscreen": "maximize",
        "full screen": "maximize",
        "normal": "restore",
        "screen shot": "screenshot",
        "take screen shot": "take screenshot",
        "capture": "capture screen",
        "listen": "play",
        "listen to": "play",
        "note": "notepad",
        "calc": "calculator",
        "paint": "mspaint",
        "vs": "vscode",
        "vs code": "vscode",
        "visual studio code": "vscode",
        "chrome browser": "chrome",
        "linkdin": "linkedin",
        "linked in": "linkedin",
    }

    @classmethod
    def _assistant_names(cls) -> set[str]:
        names = {"jarvis", "bluexech", "bluepilot", "pilot"}
        wake = (Config.WAKE_WORD or "").lower().strip()
        if wake:
            names.add(wake)
        name = (Config.ASSISTANT_NAME or "").lower().strip()
        if name:
            names.add(name)
        return names

    @classmethod
    def normalize(cls, command: str) -> str:
        command = command.lower().strip()

        # Phrase-level aliases first
        for old, new in sorted(cls.PHRASE_ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
            if old in command:
                command = command.replace(old, new)

        parts = [w.strip(".,!?") for w in command.split() if w.strip(".,!?")]

        # Only strip leading greetings + assistant name
        # e.g. "hey bluexech open chrome" -> "open chrome"
        # but keep "open bluexech" / "create bluexech website"
        assistant_names = cls._assistant_names()
        while parts and parts[0] in cls.GREETINGS:
            parts.pop(0)
        if len(parts) >= 2 and parts[0] in assistant_names:
            parts.pop(0)

        # Remove filler words (but never remove meaningful targets)
        keep_my = any("linkedin" in p for p in parts)
        cleaned: list[str] = []
        for word in parts:
            if word in cls.FILLER_WORDS:
                continue
            if word == "my" and not keep_my:
                continue
            cleaned.append(word)

        command = " ".join(cleaned)

        for old, new in sorted(cls.ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
            command = command.replace(old, new)

        return command.strip()
