"""SQLite connection handling and schema creation."""
import os
import sqlite3
from typing import Iterator

DB_PATH = os.getenv("DATABASE_PATH", "books.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    title          TEXT    NOT NULL,
    author         TEXT    NOT NULL,
    isbn           TEXT    NOT NULL UNIQUE,
    published_year INTEGER NOT NULL,
    price          REAL    NOT NULL,
    in_stock       INTEGER NOT NULL DEFAULT 1
);
"""


def init_db() -> None:
    """Create tables if they don't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA)


def get_db() -> Iterator[sqlite3.Connection]:
    """FastAPI dependency: yields a connection and always closes it."""
    # check_same_thread=False: FastAPI may run sync dependencies and
    # endpoints in different worker threads.
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()
