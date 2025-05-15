# app/utils/db.py
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB")
        )
        if connection.is_connected():
            print("Successfully connected to the MySQL database.")
        return connection
    except mysql.connector.Error as e:
        print(f"Database connection failed: {e}")
        return None
