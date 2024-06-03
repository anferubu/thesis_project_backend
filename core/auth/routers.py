from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from core.auth.utils import create_access_token, authenticate
from fastapi.security import OAuth2PasswordRequestForm

from core.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.auth.dependencies import CurrentUser
from core.auth.models import User
from core.auth.schemas import Token, UserCreate, UserRead
from core.auth.services import create_user
from core.auth.utils import create_access_token, get_user_by_email
from core.database.dependencies import DBSession



auth = APIRouter(tags=["auth"])



@auth.post("/login/access-token", response_model=Token)
async def login_for_access_token(
    session:DBSession,
    form_data:OAuth2PasswordRequestForm = Depends()
) -> Token:
    """
    """

    user = authenticate(
        session=session,
        email=form_data.username,
        password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password"
        )

    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    return Token(
        access_token=create_access_token(
            user.email, expires_delta=access_token_expires
        )
    )



@auth.get("/me", response_model=UserRead)
def read_user_me(current_user:CurrentUser) -> User:
    """
    Get current user.
    """

    return current_user



@auth.post("/register", response_model=UserRead)
async def register_user(session:DBSession, user_in:UserCreate) -> User:
    """
    """

    user = get_user_by_email(session=session, email=user_in.email)

    if user:
        raise HTTPException(status_code=400, detail="User already registered")

    user_create = UserCreate.model_validate(user_in)
    new_user = create_user(session=session, user_create=user_create)

    return new_user
