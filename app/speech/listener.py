"""
Speech Recognition service.
"""

from __future__ import annotations

import speech_recognition as sr

from app.config import Config
from app.utils.logger import logger


class Listener:
    """Handles microphone input and speech recognition."""

    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.recognizer.energy_threshold = Config.ENERGY_THRESHOLD
        self.recognizer.pause_threshold = Config.PAUSE_THRESHOLD
        self.recognizer.dynamic_energy_threshold = Config.DYNAMIC_ENERGY

        logger.info("Calibrating microphone...")

        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Microphone calibrated successfully.")
        except Exception as error:
            logger.exception("Microphone calibration failed: %s", error)

        logger.info("Speech recognizer initialized.")

    def listen(self) -> str | None:
        """
        Listen once using ONLY the active language STT.
        No cross-language fallback (avoids EN/UR mixing).
        """
        language = Config.STT_LANGUAGE
        timeout = Config.LISTEN_TIMEOUT
        phrase_limit = Config.PHRASE_TIME_LIMIT

        # Urdu phrases are often longer
        if Config.LANGUAGE == "ur":
            phrase_limit = max(phrase_limit, 10)

        try:
            with self.microphone as source:
                logger.info("Listening... (lang=%s)", language)
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit,
                )

            text = self.recognizer.recognize_google(audio, language=language)
            text = (text or "").strip()
            if not text:
                return None

            logger.info("Recognized [%s]: %s", language, text)
            return text

        except sr.WaitTimeoutError:
            logger.debug("Listening timeout.")
        except sr.UnknownValueError:
            logger.info("Speech not understood for %s.", language)
        except sr.RequestError as error:
            logger.error("Speech Recognition API Error: %s", error)
        except KeyboardInterrupt:
            logger.info("Listener interrupted.")
            raise
        except Exception:
            logger.exception("Unexpected listener error.")

        return None
