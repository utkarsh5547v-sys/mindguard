import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

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
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"I'm having trouble responding right now. Please try again. ({str(e)})"