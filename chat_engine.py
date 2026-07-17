import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma3:4b"

SYSTEM_PROMPT = """You are MindGuard, a compassionate AI mental health assistant designed to support students.

Your role:
- Listen carefully and respond with empathy and understanding
- Track the emotional tone of the conversation
- Ask gentle follow-up questions to understand the user better
- Never diagnose or prescribe — you are a supportive companion, not a doctor
- If someone expresses suicidal thoughts or crisis, always provide helpline numbers:
  iCall: 9152987821, Vandrevala Foundation: 1860-2662-345
- Keep responses concise (3-5 sentences max) — don't overwhelm the user
- Remember context from earlier in the conversation

You understand full sentences and emotional nuance, not just keywords."""


def get_response(conversation_history: list) -> str:
    """
    conversation_history = list of dicts:
    [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    """
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]
    except requests.exceptions.ConnectionError:
        return "I'm having trouble connecting right now. Please make sure Ollama is running."
    except requests.exceptions.Timeout:
        return "I'm thinking a bit slowly right now. Please try again."
    except Exception as e:
        return f"Something went wrong: {str(e)}"