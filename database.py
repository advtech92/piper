from logger import logger
import sqlite3

def init_db():
    conn = sqlite3.connect('piper.db')
    c = conn.cursor()
    # Create messages table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (content TEXT, author_id TEXT, channel_id TEXT)''')
    # Create guild introductions table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS guild_introductions
                 (guild_id TEXT UNIQUE)''')
    conn.commit()
    conn.close()

def insert_message(content, author_id, channel_id):
    try:
        conn = sqlite3.connect('piper.db')
        c = conn.cursor()
        c.execute("INSERT INTO messages VALUES (?, ?, ?)", (content, author_id, channel_id))
        conn.commit()
    except Exception as e:
        logger.error(f'Error inserting message: {e}')
    finally:
        conn.close()

def has_introduced(guild_id):
    conn = sqlite3.connect('piper.db')
    c = conn.cursor()
    c.execute("SELECT * FROM guild_introductions WHERE guild_id = ?", (guild_id,))
    result = c.fetchone()
    conn.close()
    return result is not None

def record_introduction(guild_id):
    conn = sqlite3.connect('piper.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO guild_introductions VALUES (?)", (guild_id,))
    except sqlite3.IntegrityError:
        # This means the guild_id is already recorded, which is fine since we're ensuring uniqueness
        pass
    conn.commit()
    conn.close()

# Ensure the database and its tables are initialized
init_db()