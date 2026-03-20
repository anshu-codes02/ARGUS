# 👁️ ARGUS - Voice-Activated AI Assistant

ARGUS is a Python-based, voice-activated virtual assistant designed to handle web browsing, music playback, real-time news fetching, and intelligent conversational queries. 
ARGUS leverages Google's state-of-the-art **Gemini 2.5 Flash** model for high-speed, low-latency natural language processing, making it completely free to run and highly responsive.

[![Project Demo](https://img.shields.io/badge/Watch%20Demo-Video-red?style=for-the-badge&logo=youtube)](https://drive.google.com/file/d/18A9LsLVrpARd0EKDh10YtJIQtueHgqn9/view?usp=sharing)

## ✨ Features

* **🗣️ Voice Recognition:** Listens for the wake word ("Argus") and processes natural language commands using the `speech_recognition` library.
* **🧠 Conversational AI:** Integrates the `google-genai` SDK to process complex queries with personalized system instructions for concise, assistant-like responses.
* **📰 Real-Time News:** Fetches and reads top global and local headlines using the NewsAPI `/everything` endpoint.
* **🎵 Music & Media:** Interfaces with a custom `musicLibrary` module to stream songs and opens popular websites (Google, YouTube, LinkedIn) via voice command.
* **🎙️ Natural Speech Output:** Bypasses robotic offline TTS engines by utilizing Google Text-to-Speech (`gTTS`) and `pygame` for smooth, natural audio playback.

## 🛠️ Tech Stack & Libraries

* **Core Language:** Python 3
* **AI & Brain:** `google-genai` (Gemini 2.5 Flash)
* **Speech-to-Text:** `SpeechRecognition`
* **Text-to-Speech:** `gTTS` (Google Text-to-Speech), `pygame` (Audio Mixer)
* **Web & API Integration:** `requests` (HTTP client), `webbrowser`
* **Environment Management:** `python-dotenv`, `os`

## ⚙️ System Workflow

1. **Initialization:** ARGUS boots up, loads environment variables securely, and initializes the pygame audio mixer.
2. **Wake Word Detection:** The microphone actively listens for the wake word "Argus".
3. **Command Parsing:** Once activated, it listens for the specific instruction and routes it to the appropriate module (News, Web, Music, or AI).
4. **Processing & API Calls:** - Web/Music commands open local default browsers.
   - News commands ping the NewsAPI server.
   - General questions are sent to the Gemini 2.5 API with a strict token limit to ensure low-latency replies.
5. **Audio Feedback:** The text response is saved as a temporary `.mp3` via `gTTS` and played back through `pygame`.

## 🚀 Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/anshu-codes02/ARGUS.git
cd ARGUS
```

**2. Create virtual env**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Setup .env**
```bash
GEMINI_API_KEY=your_gemini_api_key_here
NEWS_API_KEY=your_news_api_key_here
```

