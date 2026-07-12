# 🎙️ Voice-Enabled Conversational AI Agent

A Python-based voice assistant that integrates **Speech-to-Text → LLM Reasoning → Text-to-Speech** into a real-time conversational pipeline. Built to explore the practical challenges of voice interfaces and LLM API behaviour.

---

## 🧱 Architecture

```
[Microphone Input]
       ↓
[Speech-to-Text]  ← Google Speech Recognition API
       ↓            with silence detection & offline fallback
[Context Manager] ← Rolling conversation history with token budgeting
       ↓
[LLM Engine]      ← OpenAI API with prompt structuring, retry & fallback logic
       ↓
[Text-to-Speech]  ← pyttsx3 (offline) with markdown cleaning
       ↓
[Speaker Output]
```

---

## ✨ Features

- **End-to-end voice pipeline** — speak a query, hear the response
- **Push-to-talk interface** — press Enter to activate microphone
- **Silence detection** — automatically stops recording after configurable silence threshold
- **Conversation context management** — maintains multi-turn dialogue with token budget enforcement
- **Prompt structuring** — system prompt shapes response tone for spoken delivery
- **Retry & fallback logic** — handles API rate limits, connection errors, and quota exhaustion gracefully
- **Offline STT fallback** — falls back to Sphinx if Google API is unavailable
- **Markdown stripping** — cleans LLM output before TTS so responses sound natural

---

## 📂 Project Structure

```
voice-llm-assistant/
├── main.py                    # Entry point — runs the assistant loop
├── requirements.txt           # Python dependencies
├── .env.example               # API key template
└── assistant/
    ├── __init__.py
    ├── config.py              # All settings in one place
    ├── voice_input.py         # STT module (Google Speech API + fallback)
    ├── voice_output.py        # TTS module (pyttsx3 + markdown cleaner)
    ├── llm_engine.py          # OpenAI API wrapper with retry logic
    └── context_manager.py     # Conversation history + token trimming
```

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/krishnabalajikothapalli5308/voice-llm-assistant.git
cd voice-llm-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

> **Note:** PyAudio requires system-level audio libraries.
> - **Windows:** Usually works out of the box.
> - **Linux:** `sudo apt-get install portaudio19-dev python3-pyaudio`
> - **macOS:** `brew install portaudio && pip install pyaudio`

### 3. Set up your API key
```bash
cp .env.example .env
# Open .env and add your OpenAI API key
```

### 4. Run
```bash
python main.py
```

---

## 🔧 Configuration

All settings are in `assistant/config.py`:

| Setting | Default | Description |
|---|---|---|
| `MODEL_NAME` | `gpt-3.5-turbo` | OpenAI model to use |
| `MAX_TOKENS` | `300` | Max tokens per response |
| `TEMPERATURE` | `0.7` | Response creativity |
| `MAX_CONTEXT_TOKENS` | `1500` | Token budget for conversation history |
| `LISTEN_TIMEOUT` | `8s` | Wait time before giving up on speech |
| `SILENCE_THRESHOLD` | `2s` | Silence duration to end recording |
| `MAX_RETRIES` | `3` | LLM retry attempts on failure |

---

## 🔍 Key Technical Challenges Explored

### 1. Real-time speech handling
- Configuring `pause_threshold` and `energy_threshold` to balance false-trigger avoidance with responsive listening
- Gracefully handling `WaitTimeoutError` when no speech is detected

### 2. Context window management
- Token budget enforced via character-level approximation (`len(text) // 4`)
- Oldest messages trimmed automatically to stay within API limits without losing recent context

### 3. LLM API limitations
- Rate limit errors caught and retried with exponential backoff
- Authentication errors surface immediately without retry (fail-fast)
- Invalid responses handled without corrupting conversation history

### 4. Prompt structure experiments
Three prompt variants tested (see `llm_engine.py → PROMPT_VARIANTS`):
- **Concise** — 1-2 sentence answers, best for quick factual queries
- **Detailed** — thorough but conversational, better for explanatory queries
- **Socratic** — assistant asks clarifying questions before answering

Key finding: system prompt phrasing significantly affects response length and structure even with identical user queries.

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `openai` | LLM API client |
| `SpeechRecognition` | STT via Google Speech API |
| `pyttsx3` | Offline text-to-speech |
| `pyaudio` | Microphone access |
| `python-dotenv` | Environment variable management |

---

## 🚧 Limitations & Future Work

- Currently uses OpenAI API (requires key & quota)
- Offline LLM support (e.g. Ollama / LLaMA) planned
- Single language (English) — multilingual STT possible via `language` param
- No wake-word detection yet (push-to-talk only)

---

## 👤 Author

**Kothapalli Krishna Balaji**
B.Tech CSE — Bonam Venkata Chalamayya Engineering College
[GitHub](https://github.com/krishnabalajikothapalli5308) · [LinkedIn](https://www.linkedin.com/in/krishna-balaji-259a1631b)
