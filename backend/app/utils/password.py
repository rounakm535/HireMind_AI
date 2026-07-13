from app.core.security import get_password_hash, verify_password

def hash_password(password: str) -> str:
    return get_password_hash(password)

def check_password(password: str, hashed_password: str) -> bool:
    return verify_password(password, hashed_password)
