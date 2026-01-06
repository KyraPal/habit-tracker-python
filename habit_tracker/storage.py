from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from .models import Habit, Periodicity

DB_FILENAME = "habits.db"


def db_path() -> Path:
    return Path.cwd() / DB_FILENAME


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                periodicity TEXT NOT NULL CHECK(periodicity IN ('daily','weekly')),
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS checkoffs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY(habit_id) REFERENCES habits(id) ON DELETE CASCADE
            );
            """
        )


def create_habit(name: str, periodicity: Periodicity) -> Habit:
    created_at = datetime.now(timezone.utc).isoformat()
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO habits(name, periodicity, created_at) VALUES(?,?,?)",
            (name, periodicity.value, created_at),
        )
        habit_id = int(cur.lastrowid)

    return Habit(
        id=habit_id,
        name=name,
        periodicity=periodicity,
        created_at=datetime.fromisoformat(created_at),
    )


def delete_habit(name: str) -> bool:
    with connect() as conn:
        cur = conn.execute("DELETE FROM habits WHERE name = ?", (name,))
        return cur.rowcount > 0


def get_habit_by_name(name: str) -> Optional[Habit]:
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM habits WHERE name = ?", (name,)
        ).fetchone()

    if row is None:
        return None

    return Habit(
        id=int(row["id"]),
        name=str(row["name"]),
        periodicity=Periodicity(row["periodicity"]),
        created_at=datetime.fromisoformat(row["created_at"]),
    )


def list_habits() -> List[Habit]:
    with connect() as conn:
        rows = conn.execute("SELECT * FROM habits ORDER BY id ASC").fetchall()

    return [
        Habit(
            id=int(r["id"]),
            name=str(r["name"]),
            periodicity=Periodicity(r["periodicity"]),
            created_at=datetime.fromisoformat(r["created_at"]),
        )
        for r in rows
    ]


def list_habits_by(periodicity: Periodicity) -> List[Habit]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM habits WHERE periodicity = ? ORDER BY id ASC",
            (periodicity.value,),
        ).fetchall()

    return [
        Habit(
            id=int(r["id"]),
            name=str(r["name"]),
            periodicity=Periodicity(r["periodicity"]),
            created_at=datetime.fromisoformat(r["created_at"]),
        )
        for r in rows
    ]


def add_checkoff(habit: Habit, when: Optional[datetime] = None) -> None:
    ts = (when or datetime.now(timezone.utc)).isoformat()
    with connect() as conn:
        conn.execute(
            "INSERT INTO checkoffs(habit_id, timestamp) VALUES (?, ?)",
            (habit.id, ts),
        )


def list_checkoffs_for_habit(habit_id: int) -> List[datetime]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT timestamp FROM checkoffs WHERE habit_id = ? ORDER BY timestamp ASC",
            (habit_id,),
        ).fetchall()

    return [datetime.fromisoformat(r["timestamp"]) for r in rows]
