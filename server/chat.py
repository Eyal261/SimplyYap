from db.models import Message
from db.db_connection import get_db_connection


def save_message(sender_id: int, content: str, group_id: int = None, recipient_id: int = None, message_type: str = None, file_name: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (sender_id, content, group_id, recipient_id, message_type, file_name) VALUES (%s, %s, %s, %s, %s, %s)",
        (sender_id, content, group_id, recipient_id, message_type, file_name)
    )
    conn.commit()
    message_id = cursor.lastrowid
    conn.close()
    return message_id


def get_messages_for_group(group_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            m.message_id, 
            m.content AS text, 
            m.timestamp, 
            m.sender_id AS user_id, 
            u.username AS sender,
            m.message_type,
            m.file_name
        FROM messages m
        JOIN users u ON m.sender_id = u.user_id
        WHERE m.group_id = %s
        ORDER BY m.timestamp ASC
    """, (group_id,))
    
    messages = cursor.fetchall()
    conn.close()
    return messages



    