# messages_db.py
from logger import logger
import sqlite3
from database_utils import get_db_connection, is_user_excluded

def insert_message(content, author_id, channel_id):
    # Check if the user is excluded from logging
    if is_user_excluded(author_id):
        logger.info(f'Message from excluded user {author_id} not logged.')
        return

    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO messages (content, author_id, channel_id) VALUES (?, ?, ?)",
                        (content, author_id, channel_id))
            conn.commit()
    except Exception as e:
        logger.error(f'Error inserting message: {e}')
        
def increment_edit_id(edit_id):
    if not edit_id:
        return 'a'  # Start from 'a' if no edit_id is present
    
    if edit_id[-1].isdigit():  # Check if the last character is a number
        # Increment the number if the last character is a number
        base, number = edit_id[:-1], int(edit_id[-1])
        return f"{base}{number + 1}"
    else:
        # Move to the next letter or start numbering after 'z'
        if edit_id[-1] == 'z':
            return f"{edit_id}1"  # After 'z', start with 'z1'
        else:
            # Increment the letter
            return chr(ord(edit_id[-1]) + 1)

def log_message_edit(original_id, new_content, author_id, channel_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Fetch the latest edit_id for the original message
        cursor.execute("SELECT edit_id FROM messages WHERE id = ? ORDER BY timestamp DESC LIMIT 1", (original_id,))
        result = cursor.fetchone()
        
        new_edit_id = 'a'  # Default to 'a' if not found or first edit
        if result:
            last_edit_id = result[0]
            new_edit_id = increment_edit_id(last_edit_id)
        
        # Insert the edit as a new record with incremented edit_id
        conn.execute("INSERT INTO messages (content, author_id, channel_id, edit_id) VALUES (?, ?, ?, ?)",
                    (new_content, author_id, channel_id, new_edit_id))
        conn.commit()
        
# GDPR Complicance Code
def delete_message_by_user(user_id):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM messages WHERE author_id = ?", (user_id,))
        conn.commit()

def delete_message_by_guild(guild_id):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM messages WHERE channel_id IN (SELECT id FROM channels WHERE guild_id = ?)",(guild_id,))
        conn.commit()