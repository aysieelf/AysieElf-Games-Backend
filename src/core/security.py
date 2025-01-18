from passlib.context import CryptContext

# configure the password hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hash_password: str) -> bool:
    """
    Verify a plain password against its hashed version.

    Args:
        plain_password (str): The plain text password.
        hash_password (str): The hashed password.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hash_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain password.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)
