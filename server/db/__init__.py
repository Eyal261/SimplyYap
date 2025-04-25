import mysql.connector
from dotenv import load_dotenv
import os
from .db_connection import get_db_connection





def run_sql_script(cursor, script_path):
    with open(script_path, 'r') as file:
        sql = file.read()
    
    for statement in sql.split(';'):
        stmt = statement.strip()
        if stmt:
            try:
                cursor.execute(stmt)
            except Exception as e:
                print( f"[ERROR] {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("SQL script executed successfully")



if __name__ == "__main__":
    conn = get_db_connection()
    cursor = conn.cursor()

    run_sql_script(cursor, "server/db/db_functions.sql")
