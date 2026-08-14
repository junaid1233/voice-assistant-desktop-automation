"""
Professional English / Urdu response helper.
"""

from __future__ import annotations

from app.config import Config

_MESSAGES = {
    "ready": {
        "en": "Welcome. {name} is ready. How can I help you?",
        "ur": "خوش آمدید۔ {name} تیار ہے۔ میں آپ کی کیا مدد کر سکتا ہوں؟",
    },
    "goodbye": {
        "en": "Shutting down. Have a productive day.",
        "ur": "میں بند ہو رہا ہوں۔ آپ کا دن اچھا گزرے۔",
    },
    "unknown": {
        "en": "I could not match that to a supported command. Please try again clearly.",
        "ur": "یہ حکم میرے سپورٹڈ کمانڈز سے میچ نہیں ہوا۔ براہ کرم واضح طور پر دوبارہ بولیں۔",
    },
    "opening": {
        "en": "Certainly. Opening {target} now.",
        "ur": "ضرور۔ اب {target} کھول رہا ہوں۔",
    },
    "opening_failed": {
        "en": "I could not open {target}.",
        "ur": "میں {target} نہیں کھول سکا۔",
    },
    "created_folder": {
        "en": "Done. Folder created on your Desktop.",
        "ur": "ہو گیا۔ آپ کے ڈیسک ٹاپ پر فولڈر بن گیا ہے۔",
    },
    "create_failed": {
        "en": "I could not create the folder.",
        "ur": "فولڈر نہیں بن سکا۔",
    },
    "closing": {
        "en": "Closing {target} now.",
        "ur": "اب {target} بند کر رہا ہوں۔",
    },
    "screenshot_ok": {
        "en": "Screenshot captured and saved successfully.",
        "ur": "اسکرین شاٹ کامیابی سے محفوظ ہو گیا۔",
    },
    "screenshot_fail": {
        "en": "I could not capture the screenshot.",
        "ur": "اسکرین شاٹ نہیں لے سکا۔",
    },
    "playing": {
        "en": "Playing {target} now.",
        "ur": "اب {target} چلا رہا ہوں۔",
    },
    "lang_switched": {
        "en": "English mode is on. Welcome. How can I help you?",
        "ur": "اردو موڈ آن ہے۔ خوش آمدید۔ میں آپ کی کیا مدد کر سکتا ہوں؟",
    },
    "not_running": {
        "en": "{target} is not running.",
        "ur": "{target} پہلے سے بند ہے یا چل نہیں رہا۔",
    },
}


def lang() -> str:
    return Config.LANGUAGE if Config.LANGUAGE in {"en", "ur"} else "en"


def t(key: str, **kwargs) -> str:
    template = _MESSAGES.get(key, {}).get(lang()) or _MESSAGES.get(key, {}).get("en", key)
    return template.format(**kwargs)


def localize_response(response: str) -> str:
    """Ensure engine replies match the active language professionally."""
    if not response:
        return response

    text = response.strip()
    lower = text.lower()

    # Already localized keys / Urdu script replies
    if lang() == "ur" and any("\u0600" <= ch <= "\u06FF" for ch in text):
        return text

    if lower.startswith("goodbye") or "shutting down" in lower:
        return t("goodbye")
    if "could not match" in lower or "don't understand" in lower or "sorry" in lower:
        return t("unknown")
    if lower.startswith("opening ") or lower.startswith("certainly. opening"):
        # keep if already professional template
        if "certainly" in lower or "ضرور" in text:
            return text
        target = text.split("Opening", 1)[-1].strip(" .")
        return t("opening", target=target)
    if lower.startswith("created folder") or "folder created" in lower:
        return t("created_folder")
    if "screenshot saved" in lower or "screenshot captured" in lower:
        return t("screenshot_ok")
    if lower.startswith("closing "):
        target = text[8:].rstrip(".")
        return t("closing", target=target)

    # If English mode, leave English service replies as-is when already clear
    if lang() == "en":
        return text

    # Urdu mode fallback: translate common leftovers
    return text
