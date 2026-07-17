import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"

def analyze(text: str) -> dict:
    """
    Ollama se sentiment score mangao.
    Returns: {"polarity": float (-1 to 1), "label": "positive"/"neutral"/"negative"}
    """
    prompt = f"""Analyze the emotional sentiment of this message and respond with ONLY a JSON object.
Message: "{text}"
Respond with exactly this format, nothing else:
{{"polarity": 0.0, "label": "neutral"}}
Where polarity is between -1.0 (very negative) and 1.0 (very positive), and label is one of: positive, neutral, negative."""

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=30)
        
        raw = response.json()["response"].strip()
        # JSON extract karo response se
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end != 0:
            data = json.loads(raw[start:end])
            return {
                "polarity": float(data.get("polarity", 0.0)),
                "label": data.get("label", "neutral")
            }
    except Exception:
        pass
    
    return {"polarity": 0.0, "label": "neutral"}