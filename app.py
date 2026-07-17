# from flask import Flask, request, jsonify, render_template
from database import init_db, get_connection
from sentiment import analyze
from risk import check_crisis_keywords, check_mood_trend, log_alert

from flask import Flask, request, jsonify, render_template, session
from chat_engine import get_response
import os



app = Flask(__name__)
app.secret_key = "mindguard-secret-2024"  # session ke liye zaroori
# app.secret_key = os.getenv("SECRET_KEY")

init_db() 

# ─── Empathetic response logic ───────────────────────────────────────────────

RESPONSES = {
    "positive": [
        "That's great to hear! What's been going well for you?",
        "I'm glad you're feeling positive. Keep that energy going!",
    ],
    "neutral": [
        "I hear you. Sometimes things just feel flat — that's okay.",
        "Thanks for sharing. How long have you been feeling this way?",
    ],
    "negative": [
        "I'm sorry you're going through this. You're not alone.",
        "That sounds really tough. Would you like to talk more about it?",
        "It takes courage to share that. I'm here with you.",
    ],
    "crisis": (
        "I'm really concerned about what you've shared. "
        "Please reach out to iCall: 9152987821 or Vandrevala Foundation: 1860-2662-345. "
        "You don't have to face this alone."
    )
}


import random

def generate_response(text: str, sentiment_label: str) -> str:
    if check_crisis_keywords(text):
        return RESPONSES["crisis"]
    return random.choice(RESPONSES[sentiment_label])

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

    # Conversation history session mein rakho
    if "history" not in session:
        session["history"] = []

    # User message history mein add karo
    session["history"].append({"role": "user", "content": user_msg})
    
    # Last 10 messages hi rakho (memory efficient)
    if len(session["history"]) > 10:
        session["history"] = session["history"][-10:]

    # Ollama se response lo
    bot_reply = get_response(session["history"])

    # Bot response history mein add karo
    session["history"].append({"role": "assistant", "content": bot_reply})
    session.modified = True  # Flask ko batao session change hua

    # Sentiment analyze karo (background mein)
    result = analyze(user_msg)
    polarity = result["polarity"]
    label = result["label"]

    # Database mein save karo
    conn = get_connection()
    conn.execute(
        "INSERT INTO messages (role, content, sentiment) VALUES (?, ?, ?)",
        ("user", user_msg, polarity)
    )
    conn.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)",
        ("bot", bot_reply)
    )
    conn.commit()
    conn.close()

    # Crisis check
    if check_crisis_keywords(user_msg):
        log_alert(f"Crisis keywords detected: {user_msg[:50]}")

    return jsonify({
        "reply": bot_reply,
        "sentiment": label,
        "polarity": round(polarity, 2)
    })


# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.get_json()
#     user_msg = data.get("message", "").strip()
#     if not user_msg:
#         return jsonify({"error": "Empty message"}), 400

#     # Sentiment analysis
#     result = analyze(user_msg)
#     polarity = result["polarity"]
#     label = result["label"]

#     # Bot response
#     bot_reply = generate_response(user_msg, label)

#     # Save both messages
#     conn = get_connection()
#     conn.execute(
#         "INSERT INTO messages (role, content, sentiment) VALUES (?, ?, ?)",
#         ("user", user_msg, polarity)
#     )
#     conn.execute(
#         "INSERT INTO messages (role, content) VALUES (?, ?)",
#         ("bot", bot_reply)
#     )
#     conn.commit()
#     conn.close()

#     return jsonify({
#         "reply": bot_reply,
#         "sentiment": label,
#         "polarity": round(polarity, 2)
#     })


@app.route("/mood", methods=["POST"])
def log_mood():
    data = request.get_json()
    score = int(data.get("score", 5))
    note  = data.get("note", "")

    conn = get_connection()
    conn.execute(
        "INSERT INTO mood_scores (score, note) VALUES (?, ?)",
        (score, note)
    )
    conn.commit()
    conn.close()

    # Check for risk trend after logging
    trend = check_mood_trend()
    if trend["alert"]:
        log_alert(trend["reason"])

    return jsonify({"status": "saved", "alert": trend})

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return jsonify({"status": "reset"})


@app.route("/data/mood")
def mood_data():
    """Last 7 din ka mood data — dashboard ke liye."""
    conn = get_connection()
    rows = conn.execute(
        """SELECT DATE(timestamp) as day, AVG(score) as avg_score
           FROM mood_scores
           GROUP BY DATE(timestamp)
           ORDER BY day DESC
           LIMIT 7"""
    ).fetchall()
    conn.close()

    # Reverse karo taaki oldest pehle aaye (chart ke liye)
    data = [{"day": r["day"], "score": round(r["avg_score"], 1)} for r in rows]
    data.reverse()
    return jsonify(data)


@app.route("/data/chat")
def chat_history():
    conn = get_connection()
    rows = conn.execute(
        "SELECT role, content, sentiment, timestamp FROM messages ORDER BY timestamp DESC LIMIT 30"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


# ─── Run ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("MindGuard running at http://127.0.0.1:5000")
    app.run(debug=True)