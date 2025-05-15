import bcrypt
from typing import Optional, Tuple, Dict, Any
import mysql.connector
from app.utils.db import connect_to_db


def register_user(username: str, email: str, password: str) -> Tuple[bool, str]:
    conn = connect_to_db()
    if conn is None:
        return False, "Database connection failed."

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id FROM users WHERE email = %s OR username = %s",
            (email.lower(), username)
        )
        if cursor.fetchone():
            return False, "User already exists with this email or username."

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
        """, (username, email.lower(), hashed_pw))

        conn.commit()
        return True, "User registered successfully."

    except mysql.connector.Error as e:
        return False, f"MySQL error: {e}"

    finally:
        cursor.close()
        conn.close()


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    conn = connect_to_db()
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id, username, email, password_hash
            FROM users
            WHERE email = %s
        """, (email.lower(),))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode('utf-8')):
            return {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"]
            }

        return None

    except mysql.connector.Error:
        return None

    finally:
        cursor.close()
        conn.close()


def update_password(email: str, new_password: str) -> Tuple[bool, str]:
    conn = connect_to_db()
    if conn is None:
        return False, "Database connection failed."

    cursor = conn.cursor()
    try:
        hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("""
            UPDATE users SET password_hash = %s WHERE email = %s
        """, (hashed_pw, email.lower()))
        conn.commit()

        if cursor.rowcount == 0:
            return False, "No user found with this email."

        return True, "Password updated successfully."

    except mysql.connector.Error as e:
        return False, f"MySQL error: {e}"

    finally:
        cursor.close()
        conn.close()
