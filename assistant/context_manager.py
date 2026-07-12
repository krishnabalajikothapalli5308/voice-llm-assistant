"""
context_manager.py
------------------
Manages conversation history with token budget enforcement.
Prevents exceeding LLM context limits by trimming old messages.
"""


def _estimate_tokens(text: str) -> int:
    """
    Rough token estimate: ~1 token per 4 characters (OpenAI approximation).
    Used to stay within context window limits without calling the tokenizer.
    """
    return max(1, len(text) // 4)


class ConversationContext:
    """
    Stores and manages the rolling conversation history.
    Automatically trims oldest messages when the token budget is exceeded.
    """

    def __init__(self, max_tokens: int = 1500):
        self.max_tokens = max_tokens
        self._messages: list[dict] = []
        self._token_count: int = 0

    def add_message(self, role: str, content: str) -> None:
        """Add a message and trim history if over token budget."""
        tokens = _estimate_tokens(content)
        self._messages.append({
            "role": role,
            "content": content,
            "_tokens": tokens
        })
        self._token_count += tokens
        self._trim()

    def _trim(self) -> None:
        """
        Remove oldest messages (but never the system prompt) until
        the token count is within budget.
        This handles the token limit limitation of LLM APIs.
        """
        while self._token_count > self.max_tokens and len(self._messages) > 1:
            removed = self._messages.pop(0)
            self._token_count -= removed.get("_tokens", 0)
            print(f"[Context] Trimmed old message to stay within token budget.")

    def get_messages(self) -> list[dict]:
        """Return messages in the format expected by the OpenAI API."""
        return [
            {"role": m["role"], "content": m["content"]}
            for m in self._messages
        ]

    def pop_last(self) -> None:
        """Remove the last message (used on LLM error to avoid bad context)."""
        if self._messages:
            removed = self._messages.pop()
            self._token_count -= removed.get("_tokens", 0)

    def clear(self) -> None:
        """Reset the conversation."""
        self._messages = []
        self._token_count = 0

    def __len__(self) -> int:
        return len(self._messages)

    def __repr__(self) -> str:
        return f"<ConversationContext messages={len(self)} tokens≈{self._token_count}>"
