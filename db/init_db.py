import sqlite3

conn = sqlite3.connect("wired.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS wired_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    url TEXT,
    description TEXT,
    author TEXT,
    scraped_at TEXT,
    source TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database dan tabel berhasil dibuat!")