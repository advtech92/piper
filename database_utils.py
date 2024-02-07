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
    This setup supports messages, user profiles, and conversation tracking.
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