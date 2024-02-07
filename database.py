from logger import logger
import sqlite3
from contextlib import closing

def init_db():
    with closing(sqlite3.connect('piper.db')) as conn:
        with conn:
            # Create messages table if not exists
            conn.execute('''CREATE TABLE IF NOT EXISTS messages
                             (content TEXT, author_id TEXT, channel_id TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            # Create guild introductions table if not exists
            conn.execute('''CREATE TABLE IF NOT EXISTS guild_introductions
                             (guild_id TEXT UNIQUE)''')

def insert_message(content, author_id, channel_id):
    try:
        with closing(sqlite3.connect('piper.db')) as conn:
            with conn:
                conn.execute("INSERT INTO messages VALUES (?, ?, ?)", (content, author_id, channel_id))
    except Exception as e:
        logger.error(f'Error inserting message: {e}')

def has_introduced(guild_id):
    with closing(sqlite3.connect('piper.db')) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM guild_introductions WHERE guild_id = ?", (guild_id,))
        result = cursor.fetchone()
    return result is not None

def record_introduction(guild_id):
    try:
        with closing(sqlite3.connect('piper.db')) as conn:
            with conn:
                conn.execute("INSERT INTO guild_introductions VALUES (?)", (guild_id,))
    except sqlite3.IntegrityError as e:
        logger.error(f'Error recording introduction: {e}')