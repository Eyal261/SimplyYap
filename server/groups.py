from db.models import Group
from db.db_connection import get_db_connection
import random
import string


def generate_group_code(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))


def create_group(group_name: str, creator_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Generate a unique group_code
    while True:
        group_code = generate_group_code()
        cursor.execute("SELECT 1 FROM chat_groups WHERE group_code = %s", (group_code,))
        if cursor.fetchone() is None:
            break  # Code is unique

    # Insert into chat_groups
    cursor.execute(
        "INSERT INTO chat_groups (group_name, creator_id, group_code) VALUES (%s, %s, %s)",
        (group_name, creator_id, group_code)
    )
    group_id = cursor.lastrowid

    # Insert into group_members
    cursor.execute(
        "INSERT INTO group_members (group_id, user_id, is_admin) VALUES (%s, %s, %s)",
        (group_id, creator_id, True)
    )

    conn.commit()
    conn.close()
    return group_id, group_code

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


def get_group_by_group_code(group_code: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM chat_groups WHERE group_code = %s",
        (group_code,)
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
        SELECT g.group_id, g.group_name, g.creator_id, g.group_code, g.created_at
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


def get_group_members(group_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT u.user_id, u.username, gm.is_admin 
        FROM group_members gm
        JOIN users u ON gm.user_id = u.user_id
        WHERE gm.group_id = %s
    """, (group_id,)
    )
    members = cursor.fetchall()
    conn.close()
    return members


