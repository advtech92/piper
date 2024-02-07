# messages_db.py
from logger import logger
import sqlite3
from database_utils import get_db_connection

def insert_message(content, author_id, channel_id):
    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO messages (content, author_id, channel_id) VALUES (?, ?, ?)",
                         (content, author_id, channel_id))
    except Exception as e:
        logger.error(f'Error inserting message: {e}')
