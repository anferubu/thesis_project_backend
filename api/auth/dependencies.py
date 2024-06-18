"""
Define the dependencies used in the auth module.

It includes:
  - CurrentUser: get the current user.
  - LoginFormData: get the data (username and password) from the login form.

"""

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

from api.auth import exceptions as e
from api.auth.crud import get_user_by_email
from api.auth.models import User
from api.auth.security.hashing import ALGORITHM, SECRET_KEY
from core.database import DBSession



# Get the token from the header Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Dependency: Get the tokens by making a request to "/token"
AccessToken = Annotated[str, Depends(oauth2_scheme)]



async def get_current_user(session:DBSession, token:AccessToken) -> User:
    """
    Retrieve the current user based on the provided JWT access token.
    Helps us verify if the user is authenticated.

    Args:
      - session (DBSession): The database session dependency.
      - token (str): The JWT access token dependency.

    Returns:
      - User: The authenticated user.

    Raises:
      - HTTPException: If the token is invalid or the user is not found or
          inactive.
    """

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")

    if not email:
        raise e.NotAuthenticatedException()

    user = get_user_by_email(session=session, email=email)

    if not user:
        raise e.UserNotFoundException(email)

    if user.status == "inactive":
        raise e.InactiveUserException(email)

    return user



# Dependency: Get the current user according to the access token
CurrentUser = Annotated[User, Depends(get_current_user)]

# Dependency: Get the username and password of a login form
LoginFormData = Annotated[OAuth2PasswordRequestForm, Depends()]
