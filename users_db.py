# users_db.py
from logger import logger
import sqlite3
from database_utils import get_db_connection

def update_user_profile(user_id, preferences=None):
    try:
        with get_db_connection() as conn:
            conn.execute("""INSERT INTO user_profiles (user_id, preferences)
                            VALUES (?, ?)
                            ON CONFLICT(user_id)
                            DO UPDATE SET preferences = excluded.preferences""",
                         (user_id, preferences))
    except Exception as e:
        logger.error(f'Error updating user profile: {e}')
