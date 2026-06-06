"""
SQLite database helpers.
Stores search/chat history so users can revisit past queries.
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Dict

DB_PATH = os.path.join("data", "travel.db")


def get_connection() -> sqlite3.Connection:
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they don't exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS searches (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                query     TEXT    NOT NULL,
                response  TEXT    NOT NULL,
                created_at TEXT   NOT NULL
            )
            """
        )
        conn.commit()


def save_search(query: str, response: str) -> None:
    """Persist a user query and agent response."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO searches (query, response, created_at) VALUES (?, ?, ?)",
            (query, response, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()


def get_search_history(limit: int = 50) -> List[Dict]:
    """Return the most recent searches, newest first."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM searches ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(row) for row in rows]


def delete_search(search_id: int) -> None:
    """Delete a single search record."""
    with get_connection() as conn:
        conn.execute("DELETE FROM searches WHERE id = ?", (search_id,))
        conn.commit()


def clear_history() -> None:
    """Wipe all search history."""
    with get_connection() as conn:
        conn.execute("DELETE FROM searches")
        conn.commit()
