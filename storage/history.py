# prompt history
import sqlite3

DB_NAME = "users.db"


def save_prompt_history(username: str, document: str, question: str, answer: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO prompt_history (username, document, question, answer)
        VALUES (?, ?, ?, ?)
    """, (username, document, question, answer))

    conn.commit()
    conn.close()


def get_prompt_history(username: str, limit: int = 10):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT document, question, answer
        FROM prompt_history
        WHERE username = ?
        ORDER BY id DESC
        LIMIT ?
    """, (username, limit))

    rows = cursor.fetchall()
    conn.close()
    return rows
