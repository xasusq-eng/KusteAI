import sqlite3
from datetime import datetime
from pathlib import Path


class MemoryStore:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    def save_message(self, role: str, content: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO messages(role, content, created_at) VALUES (?, ?, ?)",
                (role, content, datetime.utcnow().isoformat()),
            )

    def save_memory(self, text: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO memories(text, created_at) VALUES (?, ?)",
                (text, datetime.utcnow().isoformat()),
            )

    def get_recent_messages(self, limit: int = 10) -> list[tuple[str, str]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return list(reversed(rows))

    def get_recent_memories(self, limit: int = 10) -> list[str]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT text FROM memories ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [row[0] for row in rows]
