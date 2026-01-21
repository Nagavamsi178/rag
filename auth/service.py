import sqlite3
from auth.db import DB_NAME
from security.hashing import hash_password, verify_password


def register_user(username: str, password: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Check if this is the first user
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        role = "admin" if user_count == 0 else "user"

        hashed_pw = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_pw, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def verify_user(username: str, password: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return False

    stored_hash = row[0]
    return verify_password(password, stored_hash)


def get_user_role(username: str) -> str:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()

    return row[0] if row else "user"
