import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def analyze(text: str) -> dict:
    prompt = f"""Analyze the emotional sentiment of this message and respond with ONLY a JSON object, nothing else.
Message: "{text}"
Respond with exactly this format:
{{"polarity": 0.0, "label": "neutral"}}
Where polarity is between -1.0 (very negative) and 1.0 (very positive), and label is one of: positive, neutral, negative."""

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=50
        )
        raw = completion.choices[0].message.content.strip()
        start = raw.find("{")
        end = raw.rfind("}") + 1
        data = json.loads(raw[start:end])
        return {
            "polarity": float(data.get("polarity", 0.0)),
            "label": data.get("label", "neutral")
        }
    except Exception:
        return {"polarity": 0.0, "label": "neutral"}