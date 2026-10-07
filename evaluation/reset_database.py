import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path(
    os.getenv(
        "SUPPORT_DB_PATH",
        "evaluation/evaluation.db"
    )
)

def reset_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists():
        DB_PATH.unlink()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE tickets (
            ticket_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            note TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE completed_operations (
            operation_id TEXT PRIMARY KEY
        )
    """)

    cursor.execute("""
        INSERT INTO tickets
        (ticket_id, status, note)
        VALUES (?, ?, ?)
    """, (
        "TICK-001",
        "OPEN",
        "Customer reported a duplicate charge."
    ))

    connection.commit()
    connection.close()

    print(f"Evaluation database reset: {DB_PATH}")