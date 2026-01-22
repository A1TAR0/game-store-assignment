from werkzeug.security import generate_password_hash, check_password_hash
import secrets

def hash_password(password):
    """Hash a password for storing"""
    return generate_password_hash(password)

def verify_password(password_hash, password):
    """Verify a stored password against one provided by user"""
    return check_password_hash(password_hash, password)

def generate_session_token():
    """Generate a secure random session token"""
    return secrets.token_hex(32)