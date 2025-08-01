import sqlite3
from datetime import datetime
import os

DB_PATH = os.getenv("DATABASE_PATH", "db.sqlite3")  # Varsayılan: db.sqlite3

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        original_code TEXT NOT NULL,
        analysis_result TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def save_analysis(code: str, result: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO analyses (timestamp, original_code, analysis_result) VALUES (?, ?, ?)",
                   (datetime.now().isoformat(), code, result))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, original_code, analysis_result FROM analyses ORDER BY id DESC LIMIT 20")
    history = cursor.fetchall()
    conn.close()
    return history

def delete_analysis(analysis_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted_count > 0

def delete_all_analyses():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analyses")
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted_count
