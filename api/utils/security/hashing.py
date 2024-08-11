"""
Provides functions for password hashing and verification.

It includes:
  - verify_password()
  - get_password_hash()

"""

from passlib.context import CryptContext
from core.secrets import env



SECRET_KEY = env.secret_key
ALGORITHM = "HS256"


# Password context for bcrypt hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def verify_password(plain_password, hashed_password):
    """
    Verify a password against a hashed password.

    Args:
      - plain_password (str): Plain text password.
      - hashed_password (str): Hashed password to compare against.

    Returns:
      - bool: True if the passwords match, False otherwise.
    """

    return pwd_context.verify(plain_password, hashed_password)



def get_password_hash(password:str) -> str:
    """
    Generate a hash for a given password.

    Args:
      - password (str): Password to hash.

    Returns:
      - str: Hashed password.
    """

    return pwd_context.hash(password)
