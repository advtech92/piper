# database_utils.py
import sqlite3
from contextlib import closing

DATABASE_PATH = 'piper.db'

def get_db_connection():
    """Returns a connection object for the database that can be used in a context manager."""
    return closing(sqlite3.connect(DATABASE_PATH))

def init_db():
    """
    Initializes the database by creating tables if they do not already exist.
    This setup supports messages, user profiles, conversation tracking, and excluded users.
    """
    with get_db_connection() as conn:
        with conn:
            # Create messages table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT,
                    author_id TEXT,
                    channel_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create user profiles table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id TEXT PRIMARY KEY,
                    preferences TEXT,
                    interaction_count INTEGER DEFAULT 0,
                    last_interaction DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create conversations table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id TEXT,
                    start_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    end_timestamp DATETIME,
                    topic TEXT
                )
            ''')

            # Create guild introductions table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS guild_introductions (
                    guild_id TEXT UNIQUE,
                    guild_name TEXT
                )
            ''')

            # Create excluded users table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS excluded_users (
                    user_id TEXT PRIMARY KEY
                )
            ''')

def is_user_excluded(user_id):
    """
    Checks if a given user_id is in the excluded_users table.
    
    Parameters:
    - user_id (str): The Discord ID of the user to check.
    
    Returns:
    - bool: True if the user is excluded, False otherwise.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM excluded_users WHERE user_id = ?", (user_id,))
        return cursor.fetchone() is not None

def add_user_to_excluded(user_id):
    """Adds a user to the excluded_users table."""
    with get_db_connection() as conn:
        conn.execute("INSERT INTO excluded_users (user_id) VALUES (?) ON CONFLICT(user_id) DO NOTHING", (user_id,))

def remove_user_from_excluded(user_id):
    """Removes a user from the excluded_users table."""
    with get_db_connection() as conn:
        conn.execute("DELETE FROM excluded_users WHERE user_id = ?", (user_id,))
