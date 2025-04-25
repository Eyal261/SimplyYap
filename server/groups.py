from db.models import Group
from db.db_connection import get_db_connection


def create_group(group_name: str, creator_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_groups (group_name, creator_id) VALUES (%s, %s)",
        (group_name, creator_id)
    )
    group_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO group_members (group_id, user_id, is_admin) VALUES (%s, %s, %s)",
        (group_id, creator_id, True)
    )
    conn.commit()
    conn.close()
    return group_id

def add_user_to_group(group_id: int, user_id: int, is_admin: bool = False):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO group_members (group_id, user_id, is_admin) VALUES (%s, %s, %s)",
        (group_id, user_id, is_admin)
    )
    conn.commit()
    conn.close()


def get_group_by_id(group_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM chat_groups WHERE group_id = %s",
        (group_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return Group(*row)
    return None


def remove_user_from_group(group_id: int, user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM group_members WHERE group_id = %s AND user_id = %s",
        (group_id, user_id)
    )
    conn.commit()
    conn.close()


def get_user_groups(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT g.group_id, g.group_name, g.created_at 
        FROM chat_groups g
        JOIN group_members gm ON g.group_id = gm.group_id
        WHERE gm.user_id = %s
        ORDER BY g.created_at DESC
    """, (user_id,)) 
    groups = cursor.fetchall()
    conn.close()
    return groups


def is_user_in_group(group_id: int, user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM group_members WHERE group_id = %s AND user_id = %s",
        (group_id, user_id)
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0




