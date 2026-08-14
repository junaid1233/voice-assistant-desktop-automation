"""
Text-to-Speech service.

Uses Microsoft Edge Neural Voices.
"""

from __future__ import annotations

import asyncio
import time
import uuid
from pathlib import Path

import edge_tts
import pygame

from app.config import Config
from app.utils.logger import logger


class Speaker:
    """Handles text-to-speech."""

    def __init__(self) -> None:

        self.voice = Config.VOICE_NAME
        self.volume = Config.VOICE_VOLUME

        self.temp_dir = (
            Path(__file__).resolve().parent.parent.parent
            / "temp"
        )
        self.temp_dir.mkdir(exist_ok=True)

        self.audio_file = self.temp_dir / "speech.mp3"

        try:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(self.volume)
            logger.info("Speaker initialized (%s).", self.voice)
        except Exception:
            logger.exception("Failed to initialize pygame mixer.")

    async def _generate_audio(self, text: str, path: Path) -> None:
        # Always use current language voice from Config
        self.voice = Config.VOICE_NAME
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
        )
        await communicate.save(str(path))

    def _safe_unlink(self, path: Path) -> None:
        try:
            if path.exists():
                path.unlink()
        except PermissionError:
            # Windows may keep the file locked briefly after playback
            pass
        except Exception:
            pass

    def speak(self, text: str) -> None:
        if not text:
            return

        logger.info("Speaking: %s", text)

        # Unique file avoids Windows lock on the previous speech.mp3
        audio_path = self.temp_dir / f"speech_{uuid.uuid4().hex}.mp3"

        try:
            self.stop()

            asyncio.run(self._generate_audio(text, audio_path))

            pygame.mixer.music.load(str(audio_path))
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(20)

            self.stop()
            time.sleep(0.05)
            self._safe_unlink(audio_path)

        except Exception:
            logger.exception("Speech synthesis failed.")
            self._safe_unlink(audio_path)

    def stop(self) -> None:
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                try:
                    pygame.mixer.music.unload()
                except Exception:
                    pass
        except Exception:
            pass

    def set_volume(self, volume: float) -> None:
        self.volume = max(0.0, min(1.0, volume))
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(self.volume)

    def cleanup(self) -> None:
        try:
            self.stop()
            if pygame.mixer.get_init():
                pygame.mixer.quit()

            for path in self.temp_dir.glob("speech*.mp3"):
                self._safe_unlink(path)

            logger.info("Speaker cleaned up.")
        except Exception:
            logger.exception("Cleanup failed.")
