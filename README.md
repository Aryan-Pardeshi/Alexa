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
- 📰 News headlines (NewsAPI)
- 🎵 Spotify search and playback (via Spotipy)
- 🖼️ Screenshot capture (with timestamped filename)
- 🎲 Fun extras: jokes, roasts, dice rolls, coin flips
- 🧑‍💻 GPT-powered code generation and Q&A

---

## ✏️ Edit This Project Online

[![Edit in VS Code](https://img.shields.io/badge/Edit%20in-VSCode.dev-blue?logo=visualstudiocode&style=for-the-badge)](https://vscode.dev/github/Aryan-Pardeshi/Alexa-Voice-Assistant)

---

## 📦 Project Structure

```
📦 Alexa-Voice-Assistant/
├── main.py                # Main assistant logic
├── config.py              # Static configuration
├── .env                   # API keys (DO NOT COMMIT THIS)
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

```env
GIT_TOKEN=your_azure_token
WEATHER_API=your_openweather_key
NEWS_API=your_newsapi_key
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
```

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
* `NewsAPI` + `OpenWeatherMap API`
* `pyautogui` for screenshots
* `python-dotenv` for secure token loading

---

## ⚙️ Environment Config (`.env` Example)

```env
GIT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxx
WEATHER_API=xxxxxxxxxxxxxxxxxxx
NEWS_API=xxxxxxxxxxxxxxxxxxx
SPOTIPY_CLIENT_ID=xxxxxxxxxxxxxxxxxxx
SPOTIPY_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxx
```

---

## 🙋 Author

Made with passion by [**Aryan Pardeshi**](https://github.com/Aryan-Pardeshi)

> “I built this assistant to learn, improve, and control my world using code.”

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

## ⭐ Support & Contributions

If you like this project:

* 🌟 Star it
* 🍴 Fork it
* 🧠 Suggest a feature
* 🐛 Report a bug

Let's build smarter assistants together!

