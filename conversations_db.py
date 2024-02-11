# conversations_db.py
from logger import logger
import sqlite3
from database_utils import get_db_connection

def start_conversation(channel_id, topic):
    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO conversations (channel_id, start_timestamp, topic) VALUES (?, CURRENT_TIMESTAMP, ?)",
                        (channel_id, topic))
            conn.commit()
    except Exception as e:
        logger.error(f'Error starting conversation: {e}')