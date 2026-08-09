import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    conn.commit()


def get_user_by_id(user_id):
    from src.user import User

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return User(id=row["id"], name=row["name"], role=row["role"])


def seed_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        sample_users = [
            (1, "Alice Chen", "non-viewer"),
            (2, "Bob Martinez", "viewer"),
            (3, "Carol White", "viewer"),
            (4, "David Kim", "non-viewer"),
            (5, "Eva Santos", "viewer"),
        ]
        cursor.executemany("INSERT INTO users (id, name, role) VALUES (?, ?, ?)", sample_users)
        conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    seed_db()
