import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.
    Returns the connection object if successful, None otherwise. 
    """

    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    

if __name__ == '__main__':
    conn = get_db_connection()
    if conn and conn.is_connected():
        print("Successfully connected to the database!")
        conn.close()