"""
voice_input.py
--------------
Speech-to-Text module using Google Speech Recognition API.
Handles microphone input, silence detection, and recognition errors.
"""

import speech_recognition as sr


def listen(timeout: int = 8, silence_threshold: int = 2) -> str | None:
    """
    Captures audio from the microphone and converts it to text.

    Args:
        timeout           : Max seconds to wait for the user to start speaking.
        silence_threshold : Seconds of silence that end the recording.

    Returns:
        Transcribed text string, or None on failure.
    """
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = silence_threshold  # Silence detection
    recognizer.energy_threshold = 300               # Mic sensitivity

    with sr.Microphone() as source:
        # Adjust for ambient noise on first listen
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            print("[STT] No speech detected within timeout.")
            return None

    # --- Recognition with graceful fallback ---
    try:
        text = recognizer.recognize_google(audio, language="en-IN")
        return text.strip()

    except sr.UnknownValueError:
        print("[STT] Could not understand audio.")
        return None

    except sr.RequestError as e:
        print(f"[STT] Google Speech API error: {e}")
        # Fallback: try Sphinx (offline) if available
        try:
            text = recognizer.recognize_sphinx(audio)
            print("[STT] Used offline fallback (Sphinx).")
            return text.strip()
        except Exception:
            print("[STT] Offline fallback also failed.")
            return None
