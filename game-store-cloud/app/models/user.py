from app.utils.db_sql import get_sql_connection
from app.utils.security import hash_password, verify_password
from datetime import datetime

class User:
    def __init__(self, user_id=None, email=None, username=None, password_hash=None):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.password_hash = password_hash
    
    @staticmethod
    def create(email, username, password):
        """Create a new user"""
        conn = get_sql_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        try:
            cursor.execute(
                "INSERT INTO users (email, username, password_hash) VALUES (%s, %s, %s) RETURNING user_id",
                (email, username, password_hash)
            )
            user_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            return User(user_id=user_id, email=email, username=username)
        except Exception as e:
            conn.rollback()
            cursor.close()
            conn.close()
            raise e
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        conn = get_sql_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT user_id, email, username, password_hash FROM users WHERE email = %s",
            (email,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            return User(user_id=row[0], email=row[1], username=row[2], password_hash=row[3])
        return None
    
    def verify_password(self, password):
        """Verify password against hash"""
        return verify_password(self.password_hash, password)
    
    def update_last_login(self):
        """Update last login timestamp"""
        conn = get_sql_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE users SET last_login = %s WHERE user_id = %s",
            (datetime.now(), self.user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()