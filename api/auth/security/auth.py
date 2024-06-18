"""
Provides functions for authenticating users by email and password.

It includes:
  - authenticate()

"""

from sqlmodel import Session

from api.auth.crud import get_user_by_email
from api.auth.models import User
from api.auth.security.hashing import verify_password



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
