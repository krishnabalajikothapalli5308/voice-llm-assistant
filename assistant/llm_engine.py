"""
llm_engine.py
-------------
Handles all LLM API interactions.
Features:
  - Prompt structuring with system message
  - Retry logic on API failure
  - Token limit management
  - Graceful fallback responses
"""

import time
import openai
from assistant.config import Config


class LLMEngine:
    def __init__(self, config: Config):
        self.config = config
        openai.api_key = config.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=config.OPENAI_API_KEY)

    def _build_messages(self, conversation: list[dict]) -> list[dict]:
        """
        Prepends the system prompt to the conversation history.
        This structures the prompt for better, more consistent responses.
        """
        return [
            {"role": "system", "content": self.config.SYSTEM_PROMPT}
        ] + conversation

    def generate(self, conversation: list[dict]) -> tuple[str | None, int]:
        """
        Sends conversation history to the LLM and returns a response.

        Args:
            conversation: List of {"role": ..., "content": ...} dicts.

        Returns:
            (response_text, tokens_used) or (None, 0) on total failure.
        """
        messages = self._build_messages(conversation)
        last_error = None

        for attempt in range(1, self.config.MAX_RETRIES + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.config.MODEL_NAME,
                    messages=messages,
                    max_tokens=self.config.MAX_TOKENS,
                    temperature=self.config.TEMPERATURE,
                )
                text = response.choices[0].message.content.strip()
                tokens = response.usage.total_tokens
                return text, tokens

            except openai.RateLimitError:
                print(f"[LLM] Rate limit hit (attempt {attempt}/{self.config.MAX_RETRIES}). Waiting...")
                time.sleep(self.config.RETRY_DELAY * attempt)
                last_error = "rate_limit"

            except openai.APIConnectionError:
                print(f"[LLM] Connection error (attempt {attempt}). Retrying...")
                time.sleep(self.config.RETRY_DELAY)
                last_error = "connection"

            except openai.AuthenticationError:
                print("[LLM] Invalid API key. Check your .env file.")
                return None, 0

            except openai.BadRequestError as e:
                print(f"[LLM] Bad request: {e}")
                return None, 0

            except Exception as e:
                print(f"[LLM] Unexpected error: {e}")
                last_error = str(e)
                time.sleep(self.config.RETRY_DELAY)

        print(f"[LLM] All retries failed. Last error: {last_error}")
        return None, 0


# ── Prompt structure experiments ──────────────────────────────────
# Different system prompts tested during development to analyze
# how prompt structure affects LLM response quality and tone.

PROMPT_VARIANTS = {
    "concise": (
        "You are a concise voice assistant. Answer in 1-2 sentences only."
    ),
    "detailed": (
        "You are a knowledgeable assistant. Provide thorough, accurate answers "
        "but keep them conversational and easy to follow when spoken aloud."
    ),
    "socratic": (
        "You are a thoughtful assistant that helps users think through problems "
        "by asking clarifying questions before providing answers."
    ),
}
