# 🎙️ Alexa-Style AI Voice Assistant by Aryan Pardeshi

A Python-based, AI-powered voice assistant that responds to your voice, performs tasks like reminders, weather updates, music playback, screenshot capturing, code generation, and more — just say "Alexa", and she gets to work 🔥

---

## 🚀 Features

- 🧠 AI chat using GPT-4.1 Mini (via Azure)
- 🎧 Wake word detection ("Alexa")
- 🗣️ Real-time voice-to-text via SpeechRecognition
- 💬 Persistent chat memory (remembers across sessions)
- ⏰ Reminders (spoken input like “Remind me in 15 minutes”)
- 🌤️ Weather updates (OpenWeatherMap API)
- 🎵 Spotify search and playback (via Spotipy)
- 🖼️ Screenshot capture (with timestamped filename)
- 🎲 Fun extras: jokes, roasts, dice rolls, coin flips
- 🧑‍💻 GPT-powered code generation and Q&A

---

## Built with

<code><img height="30" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png"></code>

---

## 📦 Project Structure

```
📦 Alexa-Voice-Assistant/
├── main.py                # Main assistant logic
├── config.py              # Static configuration
├── requirements.txt       # Python dependencies
├── *.mp3                  # Sound effects (start, end, thinking, etc.)
├── chat_history.json      # Persistent memory file
├── **pycache**/           # Python cache files
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/Aryan-Pardeshi/Alexa-Voice-Assistant.git
cd Alexa-Voice-Assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` File

In the root directory, add your secrets:

## ⚙️ Environment Config (`.env` Example)

```env
GIT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxx
WEATHER_API=xxxxxxxxxxxxxxxxxxx
SPOTIPY_CLIENT_ID=xxxxxxxxxxxxxxxxxxx
SPOTIPY_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxx
```

---


⚠️ Make sure `.env` is included in `.gitignore`.

### 4. Run the Assistant

```bash
python main.py
```

---

## 📊 Tech Stack

* **Python 3.10+**
* GPT-4.1 Mini (via GitHub Marketplace / Azure Inference)
* `SpeechRecognition` + `Google` API
* `gTTS` + `playsound`
* `Spotipy` (Spotify API wrapper)
* `OpenWeatherMap API`
* `pyautogui` for screenshots
* `python-dotenv` for secure token loading

---



## 🙋 Author

Made with passion by [**Aryan Pardeshi**](https://github.com/Aryan-Pardeshi)

> “This is my 1st Big Project.”

---

## 🛡️ Security Warning

❗ Never commit your `.env` or API keys to GitHub.

Use `.gitignore`:

```gitignore
.env
__pycache__/
*.mp3
chat_history.json
```

---
