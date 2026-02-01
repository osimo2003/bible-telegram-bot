import sqlite3

print("📚 Adding Topics to Bible Database...")

conn = sqlite3.connect('bible.db')
cursor = conn.cursor()

# Create topics table
print("   Creating topics table...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_name TEXT NOT NULL,
        book_id INTEGER,
        chapter INTEGER,
        verse INTEGER,
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    )
''')

# Clear old topics
cursor.execute("DELETE FROM topics")

# Define topics and their verses
topics_data = {
    "salvation": [
        ("John", 3, 16),
        ("Romans", 10, 9),
        ("Ephesians", 2, 8),
        ("Acts", 4, 12),
        ("Romans", 6, 23),
        ("John", 14, 6),
        ("Titus", 3, 5),
        ("Romans", 5, 8),
        ("John", 1, 12),
        ("Acts", 16, 31),
    ],
    "love": [
        ("1 Corinthians", 13, 4),
        ("1 Corinthians", 13, 13),
        ("John", 3, 16),
        ("1 John", 4, 8),
        ("1 John", 4, 19),
        ("Romans", 8, 38),
        ("John", 15, 13),
        ("1 Peter", 4, 8),
        ("Colossians", 3, 14),
        ("1 John", 4, 7),
    ],
    "faith": [
        ("Hebrews", 11, 1),
        ("Hebrews", 11, 6),
        ("Romans", 10, 17),
        ("James", 2, 17),
        ("Galatians", 2, 20),
        ("2 Corinthians", 5, 7),
        ("Matthew", 17, 20),
        ("Mark", 11, 22),
        ("Romans", 1, 17),
        ("Ephesians", 2, 8),
    ],
    "prayer": [
        ("Philippians", 4, 6),
        ("1 Thessalonians", 5, 17),
        ("Matthew", 6, 9),
        ("James", 5, 16),
        ("Jeremiah", 29, 12),
        ("Matthew", 7, 7),
        ("1 John", 5, 14),
        ("Mark", 11, 24),
        ("Psalm", 145, 18),
        ("Romans", 8, 26),
    ],
    "hope": [
        ("Romans", 15, 13),
        ("Jeremiah", 29, 11),
        ("Romans", 8, 28),
        ("Hebrews", 6, 19),
        ("Psalm", 42, 11),
        ("Isaiah", 40, 31),
        ("Romans", 5, 5),
        ("1 Peter", 1, 3),
        ("Lamentations", 3, 24),
        ("Psalm", 39, 7),
    ],
    "peace": [
        ("John", 14, 27),
        ("Philippians", 4, 7),
        ("Isaiah", 26, 3),
        ("Romans", 5, 1),
        ("Colossians", 3, 15),
        ("Psalm", 29, 11),
        ("John", 16, 33),
        ("Romans", 8, 6),
        ("Isaiah", 9, 6),
        ("Numbers", 6, 26),
    ],
    "strength": [
        ("Philippians", 4, 13),
        ("Isaiah", 40, 31),
        ("Psalm", 27, 1),
        ("2 Corinthians", 12, 9),
        ("Deuteronomy", 31, 6),
        ("Nehemiah", 8, 10),
        ("Psalm", 46, 1),
        ("Isaiah", 41, 10),
        ("Ephesians", 6, 10),
        ("Psalm", 73, 26),
    ],
    "forgiveness": [
        ("1 John", 1, 9),
        ("Ephesians", 4, 32),
        ("Colossians", 3, 13),
        ("Matthew", 6, 14),
        ("Psalm", 103, 12),
        ("Isaiah", 1, 18),
        ("Acts", 3, 19),
        ("Hebrews", 8, 12),
        ("Mark", 11, 25),
        ("Luke", 6, 37),
    ],
    "fear": [
        ("Isaiah", 41, 10),
        ("2 Timothy", 1, 7),
        ("Psalm", 23, 4),
        ("Psalm", 27, 1),
        ("Joshua", 1, 9),
        ("Psalm", 56, 3),
        ("1 John", 4, 18),
        ("Deuteronomy", 31, 6),
        ("Psalm", 34, 4),
        ("Isaiah", 43, 1),
    ],
    "healing": [
        ("Jeremiah", 17, 14),
        ("Psalm", 103, 3),
        ("Isaiah", 53, 5),
        ("James", 5, 15),
        ("Exodus", 15, 26),
        ("Psalm", 147, 3),
        ("3 John", 1, 2),
        ("Proverbs", 4, 22),
        ("Matthew", 9, 35),
        ("1 Peter", 2, 24),
    ],
    "wisdom": [
        ("James", 1, 5),
        ("Proverbs", 3, 5),
        ("Proverbs", 2, 6),
        ("Colossians", 2, 3),
        ("Proverbs", 9, 10),
        ("Ecclesiastes", 7, 12),
        ("Proverbs", 4, 7),
        ("James", 3, 17),
        ("Proverbs", 16, 16),
        ("1 Corinthians", 1, 30),
    ],
    "anxiety": [
        ("Philippians", 4, 6),
        ("1 Peter", 5, 7),
        ("Matthew", 6, 34),
        ("Psalm", 55, 22),
        ("Isaiah", 41, 10),
        ("John", 14, 27),
        ("Psalm", 94, 19),
        ("Matthew", 11, 28),
        ("Proverbs", 12, 25),
        ("Psalm", 46, 10),
    ],
    "joy": [
        ("Nehemiah", 8, 10),
        ("Psalm", 16, 11),
        ("John", 15, 11),
        ("Romans", 15, 13),
        ("Galatians", 5, 22),
        ("James", 1, 2),
        ("Philippians", 4, 4),
        ("Psalm", 30, 5),
        ("1 Peter", 1, 8),
        ("Habakkuk", 3, 18),
    ],
    "marriage": [
        ("Genesis", 2, 24),
        ("Ephesians", 5, 25),
        ("1 Corinthians", 13, 4),
        ("Proverbs", 18, 22),
        ("Hebrews", 13, 4),
        ("Colossians", 3, 19),
        ("1 Peter", 3, 7),
        ("Ecclesiastes", 4, 9),
        ("Mark", 10, 9),
        ("Ephesians", 5, 33),
    ],
    "money": [
        ("Matthew", 6, 24),
        ("Hebrews", 13, 5),
        ("1 Timothy", 6, 10),
        ("Proverbs", 22, 7),
        ("Malachi", 3, 10),
        ("Luke", 16, 11),
        ("Proverbs", 11, 25),
        ("Ecclesiastes", 5, 10),
        ("Matthew", 6, 19),
        ("Philippians", 4, 19),
    ],
    "death": [
        ("John", 11, 25),
        ("Psalm", 23, 4),
        ("Romans", 8, 38),
        ("1 Corinthians", 15, 55),
        ("Revelation", 21, 4),
        ("Philippians", 1, 21),
        ("2 Corinthians", 5, 8),
        ("John", 14, 2),
        ("1 Thessalonians", 4, 14),
        ("Psalm", 116, 15),
    ],
    "heaven": [
        ("John", 14, 2),
        ("Revelation", 21, 4),
        ("Philippians", 3, 20),
        ("Matthew", 6, 20),
        ("1 Corinthians", 2, 9),
        ("Revelation", 21, 21),
        ("2 Corinthians", 5, 1),
        ("Colossians", 3, 2),
        ("1 Peter", 1, 4),
        ("Hebrews", 11, 16),
    ],
    "anger": [
        ("James", 1, 19),
        ("Proverbs", 15, 1),
        ("Ephesians", 4, 26),
        ("Proverbs", 14, 29),
        ("Colossians", 3, 8),
        ("Proverbs", 19, 11),
        ("Ecclesiastes", 7, 9),
        ("Psalm", 37, 8),
        ("Proverbs", 16, 32),
        ("Ephesians", 4, 31),
    ],
    "patience": [
        ("James", 1, 4),
        ("Romans", 12, 12),
        ("Galatians", 6, 9),
        ("Ecclesiastes", 7, 8),
        ("Colossians", 3, 12),
        ("Hebrews", 10, 36),
        ("Psalm", 37, 7),
        ("Proverbs", 14, 29),
        ("Isaiah", 40, 31),
        ("2 Peter", 3, 9),
    ],
    "trust": [
        ("Proverbs", 3, 5),
        ("Psalm", 37, 5),
        ("Isaiah", 26, 4),
        ("Jeremiah", 17, 7),
        ("Psalm", 56, 3),
        ("Nahum", 1, 7),
        ("Psalm", 9, 10),
        ("Psalm", 62, 8),
        ("Proverbs", 29, 25),
        ("Isaiah", 12, 2),
    ],
}

print("   Adding topic verses...")

for topic_name, verses in topics_data.items():
    for book_name, chapter, verse in verses:
        # Get book_id
        cursor.execute("SELECT book_id FROM books WHERE book_name LIKE ?", (f'%{book_name}%',))
        result = cursor.fetchone()
        
        if result:
            book_id = result[0]
            cursor.execute(
                "INSERT INTO topics (topic_name, book_id, chapter, verse) VALUES (?, ?, ?, ?)",
                (topic_name, book_id, chapter, verse)
            )
    
    print(f"   ✓ {topic_name.title()}")

conn.commit()
conn.close()

print("")
print("=" * 40)
print("✅ TOPICS ADDED SUCCESSFULLY!")
print(f"📚 Total topics: {len(topics_data)}")
print("=" * 40)
