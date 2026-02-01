import sqlite3

class BibleBot:
    
    def __init__(self):
        self.db_path = 'bible.db'
    
    def search(self, keyword, limit=5):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT b.book_name, v.chapter, v.verse, v.text
            FROM verses v
            JOIN books b ON v.book_id = b.book_id
            WHERE v.text LIKE ?
            LIMIT ?
        '''
        
        cursor.execute(query, (f'%{keyword}%', limit))
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_verse(self, book_name, chapter, verse):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT b.book_name, v.chapter, v.verse, v.text
            FROM verses v
            JOIN books b ON v.book_id = b.book_id
            WHERE b.book_name LIKE ? AND v.chapter = ? AND v.verse = ?
        '''
        
        cursor.execute(query, (f'%{book_name}%', chapter, verse))
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    def respond(self, user_input):
        results = self.search(user_input)
        
        if not results:
            return f"❌ No verses found for '{user_input}'. Try a different word!"
        
        response = f"\n📖 Found {len(results)} verse(s) for '{user_input}':\n"
        response += "=" * 45 + "\n"
        
        for book, chapter, verse, text in results:
            response += f"\n📍 {book} {chapter}:{verse}\n"
            response += f"   \"{text}\"\n"
        
        return response


# INTERACTIVE CHAT
if __name__ == "__main__":
    
    bot = BibleBot()
    
    print("")
    print("=" * 50)
    print("🙏 BIBLE BOT - Ready to help!")
    print("=" * 50)
    print("Type any word to search the Bible")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    while True:
        print("")
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("")
            print("👋 Goodbye! God bless you!")
            print("")
            break
        
        if not user_input:
            print("Please enter a word to search.")
            continue
        
        response = bot.respond(user_input)
        print(response)
