"""Password hashing with a random salt (NFR-01). Uses only the Python standard library."""
import hashlib
import secrets


def hash_password(password: str, salt: str = "") -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200_000).hex()
    return f"{salt}${digest}"


def verify_password(password: str, stored: str) -> bool:
    salt = stored.split("$")[0]
    return secrets.compare_digest(hash_password(password, salt), stored)
