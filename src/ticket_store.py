import sqlite3
from datetime import datetime


def init_db(db_path="data/tickets.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            category TEXT,
            urgency TEXT,
            answer TEXT,
            confidence TEXT,
            status TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def log_ticket(query, category, urgency, answer, confidence, status, db_path="data/tickets.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tickets (query, category, urgency, answer, confidence, status, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (query, category, urgency, answer, confidence, status, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_all_tickets(db_path="data/tickets.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_escalated_tickets(db_path="data/tickets.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE status = 'escalated' ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
    log_ticket(
        query="Test query",
        category="technical",
        urgency="low",
        answer="Test answer",
        confidence="low",
        status="escalated"
    )
    print("Ticket logged.")
    print(get_all_tickets())