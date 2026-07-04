import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mindguard.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # dict jaisi access milegi
    return conn

def init_db():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS messages (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            role      TEXT NOT NULL,          -- 'user' ya 'bot'
            content   TEXT NOT NULL,
            sentiment REAL DEFAULT 0.0,       -- -1.0 to +1.0
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS mood_scores (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            score     INTEGER NOT NULL,        -- 1 to 10
            note      TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            reason    TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()