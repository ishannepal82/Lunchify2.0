import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.
    
    Args:
        password (str): The plain text password to hash.
        
    Returns:
        bytes: The hashed password.
    """
    # Convert password to bytes
    password_bytes = password.encode('utf-8')
    
    # Generate a salt
    salt = bcrypt.gensalt()
    
    # Hash the password
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    return hashed

def check_password(password: str, hashed: bytes) -> bool:
    """
    Checks if a password matches the hashed password.
    
    Args:
        password (str): The plain text password to verify.
        hashed (bytes): The hashed password.
        
    Returns:
        bool: True if password matches, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed)