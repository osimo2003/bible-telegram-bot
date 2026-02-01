import sqlite3
import json

print("📚 Starting Bible import...")

conn = sqlite3.connect('bible.db')
cursor = conn.cursor()

cursor.execute("DELETE FROM verses")
cursor.execute("DELETE FROM books")

print("   Loading bible.json...")
with open('bible.json', 'r', encoding='utf-8-sig') as f:
    bible = json.load(f)

old_testament = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi"
]

total_verses = 0

print("   Importing books and verses...")
for book_index, book in enumerate(bible, 1):
    book_name = book['name']
    
    if book_name in old_testament:
        testament = "Old"
    else:
        testament = "New"
    
    cursor.execute(
        "INSERT INTO books (book_id, book_name, testament) VALUES (?, ?, ?)",
        (book_index, book_name, testament)
    )
    
    for chapter_num, chapter in enumerate(book['chapters'], 1):
        for verse_num, verse_text in enumerate(chapter, 1):
            cursor.execute(
                "INSERT INTO verses (book_id, chapter, verse, text) VALUES (?, ?, ?, ?)",
                (book_index, chapter_num, verse_num, verse_text)
            )
            total_verses += 1
    
    print(f"   ✓ {book_name}")

conn.commit()
conn.close()

print("")
print("=" * 40)
print("✅ IMPORT COMPLETE!")
print(f"📖 Books imported: 66")
print(f"📜 Verses imported: {total_verses}")
print("=" * 40)
