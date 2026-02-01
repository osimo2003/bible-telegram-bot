import sqlite3

def search_bible(keyword):
    conn = sqlite3.connect('bible.db')
    cursor = conn.cursor()
    
    query = '''
        SELECT b.book_name, v.chapter, v.verse, v.text
        FROM verses v
        JOIN books b ON v.book_id = b.book_id
        WHERE v.text LIKE ?
        LIMIT 10
    '''
    
    cursor.execute(query, (f'%{keyword}%',))
    results = cursor.fetchall()
    conn.close()
    
    return results


def display_results(keyword, results):
    print("")
    print("=" * 50)
    print(f"🔍 Search results for: '{keyword}'")
    print(f"📊 Found: {len(results)} verse(s)")
    print("=" * 50)
    
    if not results:
        print("No verses found. Try a different keyword!")
        return
    
    for i, (book, chapter, verse, text) in enumerate(results, 1):
        print("")
        print(f"📖 Result {i}: {book} {chapter}:{verse}")
        print(f"   \"{text}\"")
    
    print("")
    print("=" * 50)


# TEST SEARCHES
print("🧪 Testing your Bible database...")

keyword = "love"
results = search_bible(keyword)
display_results(keyword, results)

keyword = "faith"
results = search_bible(keyword)
display_results(keyword, results)

keyword = "hope"
results = search_bible(keyword)
display_results(keyword, results)
