import sqlite3
import random
from datetime import date, time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


TOKEN = "8414803318:AAGGVJwSu_QATtvFQ8IDSflrbIi8V-J6Uws"


DAILY_CHAT_IDS = [6576385344]  

# Database path
DB_PATH = "bible.db"

# Daily verse time (24-hour format)
DAILY_HOUR = 6  # 6 AM
DAILY_MINUTE = 0  # 00 minutes


# ============================================
# DATABASE FUNCTIONS
# ============================================

def search_bible(keyword, limit=5):
    """Search Bible for keyword"""
    conn = sqlite3.connect(DB_PATH)
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


def get_random_verse():
    """Get a random verse"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = '''
        SELECT b.book_name, v.chapter, v.verse, v.text
        FROM verses v
        JOIN books b ON v.book_id = b.book_id
        ORDER BY RANDOM()
        LIMIT 1
    '''
    
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    
    return result


def get_specific_verse(book_name, chapter, verse):
    """Get a specific verse like John 3:16"""
    conn = sqlite3.connect(DB_PATH)
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


def get_chapter(book_name, chapter):
    """Get all verses in a chapter"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = '''
        SELECT v.verse, v.text
        FROM verses v
        JOIN books b ON v.book_id = b.book_id
        WHERE b.book_name LIKE ? AND v.chapter = ?
        ORDER BY v.verse
    '''
    
    cursor.execute(query, (f'%{book_name}%', chapter))
    results = cursor.fetchall()
    conn.close()
    
    return results


def search_by_book(book_name, limit=10):
    """Search verses within a specific book"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = '''
        SELECT b.book_name, v.chapter, v.verse, v.text
        FROM verses v
        JOIN books b ON v.book_id = b.book_id
        WHERE b.book_name LIKE ?
        LIMIT ?
    '''
    
    cursor.execute(query, (f'%{book_name}%', limit))
    results = cursor.fetchall()
    conn.close()
    
    return results


def get_all_books():
    """Get list of all books"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT book_name, testament FROM books ORDER BY book_id")
    results = cursor.fetchall()
    conn.close()
    
    return results


def get_verse_of_the_day():
    """Get consistent verse for today"""
    today = date.today()
    seed = today.year * 10000 + today.month * 100 + today.day
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM verses")
    total = cursor.fetchone()[0]
    
    random.seed(seed)
    verse_id = random.randint(1, total)
    
    query = '''
        SELECT b.book_name, v.chapter, v.verse, v.text
        FROM verses v
        JOIN books b ON v.book_id = b.book_id
        WHERE v.id = ?
    '''
    
    cursor.execute(query, (verse_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result


def get_all_topics():
    """Get list of all topics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT topic_name FROM topics ORDER BY topic_name")
    results = cursor.fetchall()
    conn.close()
    
    return [r[0] for r in results]


def get_verses_by_topic(topic_name, limit=5):
    """Get verses for a specific topic"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = '''
        SELECT b.book_name, t.chapter, t.verse, v.text
        FROM topics t
        JOIN books b ON t.book_id = b.book_id
        JOIN verses v ON t.book_id = v.book_id AND t.chapter = v.chapter AND t.verse = v.verse
        WHERE t.topic_name = ?
        LIMIT ?
    '''
    
    cursor.execute(query, (topic_name.lower(), limit))
    results = cursor.fetchall()
    conn.close()
    
    return results


# ============================================
# BOT COMMANDS
# ============================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    
    # Save user's chat ID for daily verses
    chat_id = update.effective_chat.id
    
    welcome = f"""
🙏 *Welcome to Bible Bot!*

Your Chat ID: `{chat_id}`
_(Save this for daily verses)_

*📚 Commands:*

*Search:*
/search <word> - Search for verses
/topic <topic> - Search by topic
/topics - List all topics

*Get Verses:*
/verse John 3:16 - Get specific verse
/chapter Psalm 23 - Get full chapter
/book Romans - Browse a book
/books - List all 66 books

*Daily:*
/votd - Verse of the Day
/random - Random verse
/subscribe - Get daily verses

/help - Show all commands
"""
    await update.message.reply_text(welcome, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
📖 *Bible Bot Help*

*🔍 Search Commands:*
/search <word> - Search all verses
/topic <topic> - Search by topic
/topics - See all topics

*📍 Get Specific Verses:*
/verse John 3:16
/verse Genesis 1:1
/verse Psalm 23:1

*📄 Get Chapters:*
/chapter John 3
/chapter Psalm 23

*📚 Browse:*
/book Romans
/books - List all 66 books

*🌅 Daily:*
/votd - Verse of the Day
/random - Random verse
/subscribe - Daily auto verse

*💡 Topics Available:*
salvation, love, faith, prayer, hope, peace, strength, forgiveness, fear, healing, wisdom, anxiety, joy, marriage, money, death, heaven, anger, patience, trust
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def votd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /votd command"""
    verse = get_verse_of_the_day()
    
    if verse:
        book, chapter, verse_num, text = verse
        today = date.today().strftime("%B %d, %Y")
        response = f"🌅 *Verse of the Day*\n"
        response += f"📅 _{today}_\n\n"
        response += f"📖 *{book} {chapter}:{verse_num}*\n\n"
        response += f"_{text}_\n\n"
        response += "🙏 Have a blessed day!"
    else:
        response = "❌ Could not get verse of the day."
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def random_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /random command"""
    verse = get_random_verse()
    
    if verse:
        book, chapter, verse_num, text = verse
        response = f"🎲 *Random Verse*\n\n"
        response += f"📖 *{book} {chapter}:{verse_num}*\n\n"
        response += f"_{text}_"
    else:
        response = "❌ Could not get a random verse."
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /search command"""
    if not context.args:
        await update.message.reply_text("Please provide a word to search.\n\nExample: /search love")
        return
    
    keyword = ' '.join(context.args)
    results = search_bible(keyword)
    
    if not results:
        await update.message.reply_text(f"❌ No verses found for '{keyword}'")
        return
    
    response = f"🔍 *Found {len(results)} verse(s) for '{keyword}':*\n\n"
    
    for book, chapter, verse, text in results:
        response += f"📖 *{book} {chapter}:{verse}*\n"
        response += f"_{text}_\n\n"
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def topics_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /topics command - List all topics"""
    topics = get_all_topics()
    
    response = "📚 *Available Topics:*\n\n"
    
    for i, topic in enumerate(topics, 1):
        response += f"{i}. {topic.title()}\n"
    
    response += "\n*Usage:* /topic <name>\n"
    response += "*Example:* /topic salvation"
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def topic_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /topic command - Search by topic"""
    if not context.args:
        topics = get_all_topics()
        response = "Please provide a topic name.\n\n"
        response += "*Available topics:*\n"
        response += ", ".join([t.title() for t in topics])
        response += "\n\n*Example:* /topic salvation"
        await update.message.reply_text(response, parse_mode='Markdown')
        return
    
    topic_name = ' '.join(context.args).lower()
    results = get_verses_by_topic(topic_name)
    
    if not results:
        topics = get_all_topics()
        response = f"❌ Topic '{topic_name}' not found.\n\n"
        response += "*Available topics:*\n"
        response += ", ".join([t.title() for t in topics])
        await update.message.reply_text(response, parse_mode='Markdown')
        return
    
    response = f"📚 *Topic: {topic_name.title()}*\n\n"
    
    for book, chapter, verse, text in results:
        response += f"📖 *{book} {chapter}:{verse}*\n"
        response += f"_{text}_\n\n"
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def verse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /verse command"""
    if not context.args:
        await update.message.reply_text(
            "Please provide book, chapter and verse.\n\n"
            "Examples:\n"
            "/verse John 3:16\n"
            "/verse Genesis 1:1\n"
            "/verse Psalm 23:1"
        )
        return
    
    text = ' '.join(context.args)
    
    try:
        if ':' not in text:
            await update.message.reply_text("Please use format: /verse Book Chapter:Verse\n\nExample: /verse John 3:16")
            return
        
        parts = text.rsplit(' ', 1)
        book_name = parts[0]
        chapter_verse = parts[1]
        
        chapter, verse = chapter_verse.split(':')
        chapter = int(chapter)
        verse = int(verse)
        
    except (ValueError, IndexError):
        await update.message.reply_text("Please use format: /verse Book Chapter:Verse\n\nExample: /verse John 3:16")
        return
    
    result = get_specific_verse(book_name, chapter, verse)
    
    if result:
        book, chap, ver, text = result
        response = f"📖 *{book} {chap}:{ver}*\n\n_{text}_"
    else:
        response = f"❌ Verse not found: {book_name} {chapter}:{verse}"
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def chapter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /chapter command"""
    if not context.args:
        await update.message.reply_text(
            "Please provide book and chapter.\n\n"
            "Examples:\n"
            "/chapter John 3\n"
            "/chapter Psalm 23"
        )
        return
    
    text = ' '.join(context.args)
    
    try:
        parts = text.rsplit(' ', 1)
        book_name = parts[0]
        chapter = int(parts[1])
    except (ValueError, IndexError):
        await update.message.reply_text("Please use format: /chapter Book Chapter\n\nExample: /chapter John 3")
        return
    
    results = get_chapter(book_name, chapter)
    
    if not results:
        await update.message.reply_text(f"❌ Chapter not found: {book_name} {chapter}")
        return
    
    response = f"📖 *{book_name.title()} Chapter {chapter}*\n\n"
    
    for verse_num, text in results[:30]:
        response += f"*{verse_num}.* {text}\n\n"
    
    if len(results) > 30:
        response += f"_(Showing 30 of {len(results)} verses)_"
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def book_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /book command"""
    if not context.args:
        await update.message.reply_text(
            "Please provide a book name.\n\n"
            "Examples:\n"
            "/book John\n"
            "/book Genesis"
        )
        return
    
    book_name = ' '.join(context.args)
    results = search_by_book(book_name)
    
    if not results:
        await update.message.reply_text(f"❌ Book not found: {book_name}\n\nUse /books to see all books.")
        return
    
    response = f"📚 *Verses from {book_name.title()}:*\n\n"
    
    for book, chapter, verse, text in results:
        response += f"📖 *{book} {chapter}:{verse}*\n"
        response += f"_{text}_\n\n"
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def books_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /books command"""
    books = get_all_books()
    
    old_testament = [b[0] for b in books if b[1] == "Old"]
    new_testament = [b[0] for b in books if b[1] == "New"]
    
    response = "📚 *Bible Books*\n\n"
    response += "*Old Testament (39):*\n"
    response += ", ".join(old_testament[:20]) + "\n"
    response += ", ".join(old_testament[20:]) + "\n\n"
    response += "*New Testament (27):*\n"
    response += ", ".join(new_testament)
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /subscribe command"""
    chat_id = update.effective_chat.id
    
    response = f"""
🌅 *Daily Verse Subscription*

Your Chat ID: `{chat_id}`

To receive daily verses automatically:

1️⃣ Copy your Chat ID above
2️⃣ Contact the bot admin
3️⃣ They will add you to daily list

_Daily verses are sent at {DAILY_HOUR}:00 AM_

For now, use /votd to get today's verse!
"""
    await update.message.reply_text(response, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages"""
    keyword = update.message.text.strip()
    
    if not keyword:
        return
    
    results = search_bible(keyword)
    
    if not results:
        await update.message.reply_text(f"❌ No verses found for '{keyword}'")
        return
    
    response = f"🔍 *Found {len(results)} verse(s) for '{keyword}':*\n\n"
    
    for book, chapter, verse, text in results:
        response += f"📖 *{book} {chapter}:{verse}*\n"
        response += f"_{text}_\n\n"
    
    await update.message.reply_text(response, parse_mode='Markdown')


# ============================================
# DAILY VERSE FUNCTION
# ============================================

async def send_daily_verse(context: ContextTypes.DEFAULT_TYPE):
    """Send daily verse to all subscribers"""
    verse = get_verse_of_the_day()
    
    if not verse:
        return
    
    book, chapter, verse_num, text = verse
    today = date.today().strftime("%B %d, %Y")
    
    message = f"🌅 *Good Morning! Daily Verse*\n"
    message += f"📅 _{today}_\n\n"
    message += f"📖 *{book} {chapter}:{verse_num}*\n\n"
    message += f"_{text}_\n\n"
    message += "🙏 Have a blessed day!"
    
    for chat_id in DAILY_CHAT_IDS:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='Markdown'
            )
            print(f"✅ Daily verse sent to {chat_id}")
        except Exception as e:
            print(f"❌ Failed to send to {chat_id}: {e}")


# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Start the bot"""
    print("=" * 50)
    print("🤖 Starting Bible Bot (Full Version)...")
    print("=" * 50)
    print("")
    print("Features:")
    print("  ✅ Keyword Search")
    print("  ✅ Topic Search (20 topics)")
    print("  ✅ Verse of the Day")
    print("  ✅ Get Specific Verse")
    print("  ✅ Get Full Chapter")
    print("  ✅ Search by Book")
    print("  ✅ List All Books")
    print("  ✅ Random Verse")
    print("  ✅ Daily Auto-Send")
    print("")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    # Create application
    app = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("votd", votd_command))
    app.add_handler(CommandHandler("random", random_command))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CommandHandler("topics", topics_command))
    app.add_handler(CommandHandler("topic", topic_command))
    app.add_handler(CommandHandler("verse", verse_command))
    app.add_handler(CommandHandler("chapter", chapter_command))
    app.add_handler(CommandHandler("book", book_command))
    app.add_handler(CommandHandler("books", books_command))
    app.add_handler(CommandHandler("subscribe", subscribe_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Schedule daily verse (if chat IDs are set)
    if DAILY_CHAT_IDS:
        job_queue = app.job_queue
        job_queue.run_daily(
            send_daily_verse,
            time=time(hour=DAILY_HOUR, minute=DAILY_MINUTE),
            name="daily_verse"
        )
        print(f"📅 Daily verse scheduled for {DAILY_HOUR}:{DAILY_MINUTE:02d} AM")
    else:
        print("📅 Daily verse: No subscribers yet")
    
    print("")
    print("✅ Bible Bot is running!")
    print("Go to Telegram and test the new features!")
    print("")
    
    app.run_polling()


if __name__ == "__main__":
    main()
