"""Loads transactions.csv and budget.csv into a SQLite database (finance.db)."""
import sqlite3
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
conn = sqlite3.connect(DATA / "finance.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS transactions")
cur.execute("""
CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    date TEXT,
    department TEXT,
    type TEXT,
    category TEXT,
    amount REAL
)
""")

cur.execute("DROP TABLE IF EXISTS budget")
cur.execute("""
CREATE TABLE budget (
    budget_id INTEGER PRIMARY KEY,
    date TEXT,
    department TEXT,
    type TEXT,
    budgeted_amount REAL
)
""")

with open(DATA / "transactions.csv") as f:
    reader = csv.reader(f)
    next(reader)
    cur.executemany("INSERT INTO transactions VALUES (?,?,?,?,?,?)", reader)

with open(DATA / "budget.csv") as f:
    reader = csv.reader(f)
    next(reader)
    cur.executemany("INSERT INTO budget VALUES (?,?,?,?,?)", reader)

conn.commit()
print("Rows in transactions:", cur.execute("SELECT COUNT(*) FROM transactions").fetchone()[0])
print("Rows in budget:", cur.execute("SELECT COUNT(*) FROM budget").fetchone()[0])
conn.close()
