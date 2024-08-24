from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

from api.crud.users import get_user_by_email
from api.models.users import User
from api.utils.security.hashing import ALGORITHM, SECRET_KEY
from core.database import DBSession



# Get the token from the header Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Dependency: Get the tokens by making a request to "/token"
AccessToken = Annotated[str, Depends(oauth2_scheme)]



async def get_current_user(session:DBSession, token:AccessToken) -> User:
    """Retrieve the current user based on the provided JWT access token.
    Helps us verify if the user is authenticated."""

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(401, "Not authenticated!")
    email = payload.get("sub")
    if not email:
        raise HTTPException(401, "Not authenticated!")
    user = get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(404, f"User {email} not found!")
    if user.status == "inactive":
        raise HTTPException(403, f"User {email} is inactive!")
    return user



# Dependency: Get the current user according to the access token
CurrentUser = Annotated[User, Depends(get_current_user)]
LoginRequired = Depends(get_current_user)

# Dependency: Get the username (email) and password of a login form
LoginFormData = Annotated[OAuth2PasswordRequestForm, Depends()]
