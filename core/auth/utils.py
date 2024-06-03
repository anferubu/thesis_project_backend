from datetime import datetime, timedelta, UTC

from jose import jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from core.auth.config import ALGORITHM, SECRET_KEY
from core.auth.models import User



# Password context for bcrypt hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def create_access_token(email:str, expires_delta:timedelta) -> str:
    """
    Create a JWT access token.

    Args:
    - email (str): The user's email to encode in the token.
    - expires_delta (timedelta): The duration for which the token is valid.

    Returns:
    - str: The encoded JWT access token.
    """

    expire = datetime.now(UTC) + expires_delta
    to_encode = {"email": email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



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



def authenticate(session:Session, email:str, password:str) -> User|None:
    """
    Authenticate a user by email and password.

    Args:
    - session (Session): The database session to use for querying.
    - email (str): The email address of the user to authenticate.
    - password (str): The plain text password to verify.

    Returns:
    - User|None: The authenticated user object if credentials are valid,
      otherwise None.
    """

    user = get_user_by_email(session=session, email=email)

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user



def get_user_by_email(session:Session, email:str) -> User|None:
    """
    Retrieve a user by email.

    Args:
    - session (Session): The database session to use for querying.
    - email (str): The email address of the user to retrieve.

    Returns:
    - User|None: The user object if found, otherwise None.
    """

    query = select(User).where(User.email == email)
    result = session.exec(query).first()

    return result