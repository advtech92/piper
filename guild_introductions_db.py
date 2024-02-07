from logger import logger
import sqlite3
from database_utils import get_db_connection

def has_introduced(guild_id):
    """
    Checks if Piper has already introduced herself in the specified guild.

    Parameters:
    - guild_id: The ID of the guild to check.

    Returns:
    - True if Piper has introduced herself, False otherwise.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM guild_introductions WHERE guild_id = ?", (guild_id,))
            return cursor.fetchone() is not None
    except Exception as e:
        logger.error(f'Error checking introduction status for guild {guild_id}: {e}')
        return False  # Assume not introduced in case of error

def record_introduction(guild_id, guild_name):
    """
    Records that Piper has introduced herself in the specified guild,
    along with the guild's name for easier identification.

    Parameters:
    - guild_id: The ID of the guild.
    - guild_name: The name of the guild.
    """
    try:
        with get_db_connection() as conn:
            conn.execute("BEGIN")
            conn.execute("INSERT INTO guild_introductions (guild_id, guild_name) VALUES (?, ?) ON CONFLICT(guild_id) DO UPDATE SET guild_name = excluded.guild_name", (guild_id, guild_name))
            conn.commit()
            logger.info(f"Introduction recorded for guild: {guild_name} (ID: {guild_id})")
    except sqlite3.IntegrityError as e:
        logger.info(f"Introduction already recorded for guild {guild_id}: {e}")
    except Exception as e:
        logger.error(f"Error recording introduction for guild {guild_id}: {e}")
        # Rollback in case of error
        conn.rollback()