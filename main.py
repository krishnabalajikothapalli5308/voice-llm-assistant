"""
Voice-Enabled Conversational AI Agent
======================================
Entry point for the voice assistant pipeline.
Run this file to start the assistant.
"""

from assistant.voice_input import listen
from assistant.voice_output import speak
from assistant.llm_engine import LLMEngine
from assistant.context_manager import ConversationContext
from assistant.config import Config
import time


def main():
    config = Config()
    context = ConversationContext(max_tokens=config.MAX_CONTEXT_TOKENS)
    llm = LLMEngine(config)

    print("\n🎙️  Voice LLM Assistant Started")
    print(f"   Model  : {config.MODEL_NAME}")
    print(f"   Mode   : Push-to-Talk (press Enter to speak, Ctrl+C to quit)")
    print("-" * 50)

    speak("Hello! I'm your voice assistant. Press Enter and speak your query.")

    while True:
        try:
            input("\n[Press Enter to speak...]")

            # --- Speech-to-Text ---
            print("🎤 Listening...")
            user_text = listen(
                timeout=config.LISTEN_TIMEOUT,
                silence_threshold=config.SILENCE_THRESHOLD
            )

            if not user_text:
                speak("I didn't catch that. Please try again.")
                continue

            print(f"You: {user_text}")

            # --- Context Management ---
            context.add_message("user", user_text)
            messages = context.get_messages()

            # --- LLM Reasoning ---
            print("🤖 Thinking...")
            start = time.time()
            response, tokens_used = llm.generate(messages)
            latency = round(time.time() - start, 2)

            if response is None:
                speak("I ran into an issue. Let me try again.")
                context.pop_last()
                continue

            print(f"Assistant ({latency}s, {tokens_used} tokens): {response}")
            context.add_message("assistant", response)

            # --- Text-to-Speech ---
            speak(response)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            speak("Goodbye!")
            break
        except Exception as e:
            print(f"[Error] {e}")
            speak("Something went wrong. Please try again.")


if __name__ == "__main__":
    main()
