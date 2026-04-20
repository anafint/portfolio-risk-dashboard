import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "portfolio.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_data (
                ticker      TEXT,
                date        TEXT,
                close_price REAL,
                PRIMARY KEY (ticker, date)
            )
        """)
        conn.commit()