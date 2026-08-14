"""
Main Assistant class.
"""

from __future__ import annotations

from typing import Callable

from app.config import Config
from app.speech.listener import Listener
from app.speech.speaker import Speaker
from app.assistant.command_processor import CommandProcessor
from app.i18n import t, localize_response
from app.utils.logger import logger


class Assistant:
    """Main application coordinator."""

    def __init__(
        self,
        on_status: Callable[[str], None] | None = None,
        on_heard: Callable[[str], None] | None = None,
        on_reply: Callable[[str], None] | None = None,
    ) -> None:

        logger.info("Initializing Assistant...")

        self.on_status = on_status or (lambda _: None)
        self.on_heard = on_heard or (lambda _: None)
        self.on_reply = on_reply or (lambda _: None)

        # Lock language for this session
        self.session_language = Config.LANGUAGE
        Config.set_language(self.session_language)

        self.listener = Listener()
        self.speaker = Speaker()
        self.processor = CommandProcessor()

        self.running = False

        logger.info(
            "Assistant initialized. session_language=%s stt=%s voice=%s",
            self.session_language,
            Config.STT_LANGUAGE,
            Config.VOICE_NAME,
        )

    def stop(self) -> None:
        self.running = False
        self.on_status("Stopping...")
        logger.info("Stop requested.")

    def switch_language(self, language: str) -> None:
        """Switch language live and speak a welcome in that language."""
        Config.set_language(language)
        self.session_language = Config.LANGUAGE
        welcome = t("lang_switched")
        self.on_reply(welcome)
        # Speak on a side thread so UI doesn't freeze if called from UI thread
        try:
            self.speaker.speak(welcome)
        except Exception:
            logger.exception("Failed to speak language switch welcome.")

    def run(self) -> None:
        self.running = True

        # Re-assert language every session start
        Config.set_language(self.session_language)

        greeting = t("ready", name=Config.ASSISTANT_NAME)
        self.on_status("Running")
        self.on_reply(greeting)
        self.speaker.speak(greeting)

        logger.info("Assistant started. Language=%s", Config.LANGUAGE)

        try:
            while self.running:
                # Keep language locked during loop (UI cannot drift mid-session)
                Config.set_language(self.session_language)

                self.on_status("Listening...")
                text = self.listener.listen()

                if not self.running:
                    break

                if not text:
                    continue

                self.on_heard(text)
                response = self.processor.process(text)

                # Stay silent on empty / ignored noise
                if not response:
                    continue

                response = localize_response(response)
                self.on_reply(response)
                self.speaker.speak(response)

                lower = response.lower()
                if lower.startswith("goodbye") or "shutting down" in lower or response.startswith("میں بند"):
                    self.running = False

        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received.")
            bye = t("goodbye")
            self.on_reply(bye)
            self.speaker.speak(bye)

        except Exception:
            logger.exception("Unexpected assistant error.")
            self.on_status("Error")

        finally:
            self.running = False
            self.speaker.cleanup()
            self.on_status("Stopped")
            logger.info("Assistant shutting down.")
