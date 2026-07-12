"""
voice_output.py
---------------
Text-to-Speech module using pyttsx3 (offline, no API quota needed).
Converts assistant responses to spoken audio.
"""

import pyttsx3
import re


def _clean_text(text: str) -> str:
    """
    Strip markdown/special characters that sound odd when spoken.
    e.g. **bold**, `code`, bullet points → plain text.
    """
    text = re.sub(r'\*+', '', text)       # Remove bold/italic asterisks
    text = re.sub(r'`+', '', text)        # Remove code backticks
    text = re.sub(r'#+\s*', '', text)     # Remove markdown headers
    text = re.sub(r'[-•]\s+', '', text)   # Remove bullet points
    text = re.sub(r'\s+', ' ', text)      # Collapse whitespace
    return text.strip()


def speak(text: str, rate: int = 175, volume: float = 1.0) -> None:
    """
    Converts text to speech and plays it.

    Args:
        text   : The text to speak.
        rate   : Words per minute (default 175).
        volume : Volume level 0.0 – 1.0 (default 1.0).
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    # Prefer a clear English voice if available
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'english' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    clean = _clean_text(text)
    if clean:
        engine.say(clean)
        engine.runAndWait()
    engine.stop()
