"""
VoxControl AI - Main Application Entrypoint
Advanced Voice-Controlled Windows PC Assistant with Full Application Interaction.
"""

import os
import sys
import json
import logging
import warnings
from typing import Dict, Any

# Suppress COM threading mode warning from pywinauto
warnings.filterwarnings("ignore", message=".*Revert to STA COM threading mode.*")
warnings.filterwarnings("ignore", category=UserWarning, module="pywinauto")

from assistant.system_controller import attach_to_default_desktop
from assistant.speech_output import speech_output
from assistant.speech_input import speech_input
from ui.dashboard import VoxControlDashboard


def setup_logging():
    """Configures application-wide logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
        datefmt="%H:%M:%S"
    )


def load_config() -> Dict[str, Any]:
    """Loads configuration settings from config.json."""
    config_path = "config.json"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading config.json: {e}")
    return {}


def main():
    """Launches VoxControl AI."""
    setup_logging()
    logger = logging.getLogger("VoxControl.Main")
    logger.info("Starting VoxControl AI...")

    # Attach thread desktop to interactive user desktop
    attach_to_default_desktop()

    config = load_config()

    # Apply speech recognition configuration
    stt_conf = config.get("speech_recognition", {})
    speech_input.apply_config(stt_conf)

    # Apply TTS configuration
    tts_conf = config.get("text_to_speech", {})
    speech_output.enabled = tts_conf.get("enabled", True)
    speech_output.speech_rate = tts_conf.get("speech_rate", 180)
    speech_output.volume = tts_conf.get("volume", 0.95)

    # Initialize dashboard GUI
    app = VoxControlDashboard()

    # Initial greeting speech
    if speech_output.enabled:
        speech_output.speak("VoxControl AI initialized and ready.")

    try:
        app.mainloop()
    finally:
        logger.info("Shutting down VoxControl AI...")
        speech_input.stop_continuous_listening()
        speech_output.shutdown()


if __name__ == "__main__":
    main()
