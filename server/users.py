from db.models import User
from db.db_connection import get_db_connection
from datetime import datetime 
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(username:str, password: str, email: str):
    password_hash = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, email, created_at) VALUES (%s, %s, %s, %s)",
        (username, password_hash, email, datetime.now())
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def get_user_by_username(username:str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = %s", (username,)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return User(*row)
    return None


def verify_password(username: str, password: str):
    user = get_user_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        return user
    return False


