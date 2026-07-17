# MindGuard 🧠
### AI Mental Health Assistant for Students

MindGuard is a conversational AI assistant designed to help students manage stress, anxiety, and emotional wellbeing through empathetic dialogue and mood tracking.

---

## Features

- **AI-Powered Conversations** — Powered by Gemma 3 (4B) via Ollama. Understands full sentences and conversation context, not just keywords.
- **Sentiment Analysis** — Detects emotional tone of each message (positive / neutral / negative) in real time.
- **Daily Mood Check-in** — Log your mood (1–10) with optional notes every day.
- **Mood Trend Dashboard** — Visual 7-day mood graph built with Chart.js.
- **Risk Detection** — Automatically detects crisis keywords and low mood trends, generates alerts with helpline numbers.
- **Conversation Memory** — Bot remembers context within a session for natural, flowing conversations.
- **New Conversation Reset** — Start fresh anytime with one click.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| AI Model | Gemma 3 4B via Ollama |
| Sentiment Analysis | Ollama (LLM-based) |
| Database | SQLite |
| Frontend | HTML, CSS, Vanilla JS |
| Charts | Chart.js |
| Deployment | Render.com |

---

## Project Structure

mindguard/
├── app.py            # Flask routes and server
├── chat_engine.py    # Ollama conversation engine
├── database.py       # SQLite helper functions
├── sentiment.py      # LLM-based sentiment analysis
├── risk.py           # Crisis detection and alerts
├── requirements.txt
└── templates/
└── index.html    # Frontend (single page)

---

## How It Works

User Message
↓
Conversation History (last 10 messages)
↓
Gemma 3 4B — understands full context
↓
Empathetic Response + Sentiment Score
↓
Risk Check (crisis keywords + mood trends)
↓
SQLite — saves all messages and mood data

---

## Local Setup

**Prerequisites:** Python 3.10+, [Ollama](https://ollama.com) installed

```bash
# 1. Clone the repo
git clone https://github.com/utkarsh5547v-sys/mindguard.git
cd mindguard

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Pull the AI model
ollama pull gemma3:4b

# 5. Run the app
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

---

## Why Gemma 3 over BERT or GPT?

- Runs **fully locally** — no API costs, no data sent to external servers
- **Context-aware** — understands entire conversation, not just individual words
- **Privacy-first** — all user data stays on device
- Small enough (3.3GB) to run on a laptop with 6GB VRAM

---

## Future Scope

- PostgreSQL for persistent cloud storage
- User authentication and profiles
- BERT-based emotion classification (fine-tuned on mental health datasets)
- Mobile app (React Native)
- Weekly email mood summaries

---

## Crisis Resources

If you or someone you know is struggling:
- **iCall (India):** 9152987821
- **Vandrevala Foundation:** 1860-2662-345
- **NIMHANS:** 080-46110007

---

*Built as a portfolio project. Not a substitute for professional mental health support.*