from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from core.auth.config import ALGORITHM, SECRET_KEY, TOKEN_URL
from core.auth.models import User
from core.auth.schemas import TokenPayload
from core.auth.utils import get_user_by_email
from core.database.dependencies import DBSession



oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)
AccessToken = Annotated[str, Depends(oauth2_scheme)]



async def get_current_user(session:DBSession, token:AccessToken) -> User:
    """
    Retrieve the current user based on the provided JWT access token.

    Args:
    - session (DBSession): The database session dependency.
    - token (str): The JWT access token dependency.

    Returns:
    - User: The authenticated user.

    Raises:
    - HTTPException: If the token is invalid or the user is not found or
      inactive.
    """

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)

        print("TOKEN DATA", token_data)

    except (JWTError, ValidationError):
        # Raise HTTP 403 if the token is invalid
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    # Retrieve the user from the database
    user = get_user_by_email(session=session, email=token_data.email)
    user = session.get(User, user.id)

    if not user:
        # Raise HTTP 404 if the user is not found
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        # Raise HTTP 400 if the user is inactive
        raise HTTPException(status_code=400, detail="Inactive user")

    return user



CurrentUser = Annotated[User, Depends(get_current_user)]