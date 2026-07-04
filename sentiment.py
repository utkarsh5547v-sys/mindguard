from textblob import TextBlob

EMOTIONAL_WORDS = {
    "sad", "happy", "anxious", "stressed", "depressed", "great",
    "terrible", "lonely", "excited", "scared", "hopeless", "good",
    "bad", "tired", "angry", "calm", "worried", "fine", "awful"
}

def analyze(text: str) -> dict:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    words = set(text.lower().split())

    has_emotional_word = bool(words & EMOTIONAL_WORDS)

    if not has_emotional_word:
        return {"polarity": 0.0, "label": "neutral"}

    if polarity > 0.2:
        label = "positive"
    elif polarity < -0.2:
        label = "negative"
    else:
        label = "neutral"

    return {"polarity": polarity, "label": label}