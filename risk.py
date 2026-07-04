from database import get_connection

CRISIS_KEYWORDS = [
    "want to die", "kill myself", "end it", "no point",
    "hopeless", "can't go on", "suicide"
]

def check_crisis_keywords(text: str) -> bool:
    text_lower = text.lower()
    return any(kw in text_lower for kw in CRISIS_KEYWORDS)

def check_mood_trend() -> dict:
    """Last 3 din ke scores dekho. Agar teenon < 4 hain toh alert."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT score FROM mood_scores ORDER BY timestamp DESC LIMIT 3"
    ).fetchall()
    conn.close()

    if len(rows) < 3:
        return {"alert": False, "reason": None}

    scores = [r["score"] for r in rows]
    if all(s <= 4 for s in scores):
        return {
            "alert": True,
            "reason": f"Mood consistently low: {scores}. Please reach out for support."
        }
    return {"alert": False, "reason": None}

def log_alert(reason: str):
    conn = get_connection()
    conn.execute("INSERT INTO alerts (reason) VALUES (?)", (reason,))
    conn.commit()
    conn.close()