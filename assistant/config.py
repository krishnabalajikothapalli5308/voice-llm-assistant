"""
Configuration settings for the Voice LLM Assistant.
Update API keys and preferences here.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # --- LLM Settings ---
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    MAX_TOKENS: int = 300          # Max tokens per LLM response
    TEMPERATURE: float = 0.7       # Response creativity (0 = precise, 1 = creative)

    # --- Context Settings ---
    MAX_CONTEXT_TOKENS: int = 1500  # Approximate token budget for conversation history
    SYSTEM_PROMPT: str = (
        "You are a helpful, concise voice assistant. "
        "Keep your responses brief and conversational since they will be spoken aloud. "
        "Avoid using bullet points, markdown, or special characters."
    )

    # --- STT Settings ---
    LISTEN_TIMEOUT: int = 8         # Max seconds to wait for speech
    SILENCE_THRESHOLD: int = 2      # Seconds of silence before stopping recording

    # --- TTS Settings ---
    TTS_RATE: int = 175             # Speech rate (words per minute)
    TTS_VOLUME: float = 1.0         # Volume (0.0 to 1.0)

    # --- Fallback Settings ---
    MAX_RETRIES: int = 3            # Max LLM call retries on failure
    RETRY_DELAY: float = 1.5        # Seconds between retries
