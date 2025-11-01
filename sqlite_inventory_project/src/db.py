# db.py — database connection and initialization helpers

import os
import sqlite3
from contextlib import contextmanager

# Paths are resolved relative to this file so running from anywhere works.
PKG_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(PKG_ROOT)

DB_PATH = os.path.join(PROJECT_ROOT, "inventory.db")
SCHEMA_PATH = os.path.join(PROJECT_ROOT, "data", "schema.sql")
SAMPLE_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "sample_data.sql")

def initialize_database() -> None:
    """Create the database and tables if missing."""
    os.makedirs(PROJECT_ROOT, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn, open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
        conn.commit()

def load_sample_data() -> None:
    """(Optional) Load sample data for quick demos."""
    with sqlite3.connect(DB_PATH) as conn, open(SAMPLE_DATA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
        conn.commit()

@contextmanager
def get_connection():
    """
    Yields a SQLite connection with:
    - row_factory for dict-like access,
    - foreign_keys pragma enabled,
    and ensures commit/rollback/close lifecycle.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
