import sqlite3

print("🔨 Creating database...")

conn = sqlite3.connect('bible.db')
cursor = conn.cursor()

print("   Creating books table...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY,
        book_name TEXT NOT NULL,
        testament TEXT
    )
''')

print("   Creating verses table...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS verses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        chapter INTEGER,
        verse INTEGER,
        text TEXT,
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    )
''')

conn.commit()
conn.close()

print("✅ Database created successfully!")
print("📁 File saved as: bible.db")
