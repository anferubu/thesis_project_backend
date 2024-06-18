"""
Define the endpoints for the auth module.

Includes:
  - POST /token
  - POST /refresh-token
  - POST /register
  - GET /confirm-email/{token}
  - POST /change-password
  - POST /request-password-reset
  - POST /reset-password/{token}

"""

from fastapi import APIRouter, BackgroundTasks, Request
from pydantic import EmailStr

from api.auth import crud, exceptions as e
from api.auth.dependencies import CurrentUser, LoginFormData
from api.auth.models import User
from api.auth.schemas import PasswordChange, Token, UserCreate, UserRead, RequestPasswordReset
from api.auth.security import jwt
from api.auth.security.auth import authenticate
from api.auth.security.hashing import verify_password, get_password_hash
from core.database import DBSession
from core.email import send_email



router = APIRouter()



@router.post("/token", response_model=Token)
async def login_for_access_token(
    session:DBSession, form_data:LoginFormData
) -> Token:
    """
    Authenticates the user and provides an access token and a refresh token.
    This endpoint takes the user's login credentials (email and password),
    authenticates them against the database, and returns a JWT access token and
    refresh token if the credentials are valid.

    Args:
      - session (DBSession): The database session to use for authentication.
      - form_data (LoginFormData): The form data containing the user's username
          (email) and password.

    Returns:
      - Token: A Token object containing the access token and refresh token.

    Raises:
      - HTTPException: If the credentials are incorrect or the user is
          inactive, an HTTPException is raised with an appropriate error
          message.
    """

    user = authenticate(
        session=session, email=form_data.username, password=form_data.password
    )

    if not user:
        raise e.IncorrectCredentialsException()

    elif user.status == "inactive":
        raise e.InactiveUserException(user.email)

    return Token(
        access_token=jwt.create_access_token(user.email),
        refresh_token=jwt.create_refresh_token(user.email)
    )



@router.post("/refresh-token", response_model=Token)
async def refresh_access_token(refresh_token:str) -> Token:
    """
    Refreshes the access token using the provided refresh token. This endpoint
    decodes the provided refresh token to extract the user's email and
    generates a new access token and refresh token.

    Args:
      - refresh_token (str): The refresh token used to generate new tokens.

    Returns:
      - Token: A Token object containing the new access token and refresh
          token.

    Raises:
      - HTTPException: If the token is invalid or cannot be decoded, an
          HTTPException is raised with an appropriate error message.
    """

    payload = jwt.decode_token(refresh_token)
    email = payload.get("sub")

    if not email:
        raise e.InvalidTokenException()

    return Token(
        access_token=jwt.create_access_token(email),
        refresh_token=jwt.create_refresh_token(email)
    )



@router.get("/users/me", response_model=UserRead)
def read_user_me(current_user:CurrentUser) -> User:
    """
    Retrieves the current authenticated user's information. This endpoint
    returns the details of the currently authenticated user.

    Args:
      - current_user (CurrentUser): The current authenticated user object.

    Returns:
      - User: The current user's details.
    """

    return current_user



@router.post("/register", response_model=UserRead)
async def register_user(
    session:DBSession,
    user_in:UserCreate,
    background_tasks:BackgroundTasks,
    request:Request
) -> User:
    """
    Registers a new user and sends a confirmation email. This endpoint
    registers a new user with the provided details, adds the user to the
    database, and sends a confirmation email with a token to verify their
    email address.

    Args:
      - session (DBSession): The database session to use for user creation.
      - user_in (UserCreate): The user details for registration.
      - background_tasks (BackgroundTasks): Background tasks to handle sending
          emails.

    Returns:
      - User: The newly registered user's details.

    Raises:
      - HTTPException: If the email is already registered, an HTTPException is
          raised with an appropriate error message.
    """

    user = crud.get_user_by_email(session=session, email=user_in.email)

    if user:
        print("USER.EMAIL", user.email)
        raise e.UserAlreadyRegisteredException(user.email)

    user_create = UserCreate.model_validate(user_in)
    new_user = crud.create_user(session=session, user_create=user_create)

    confirmation_token = jwt.create_confirmation_token(new_user.email)

    domain = f"{request.url.scheme}://{request.headers['host']}"
    confirmation_link = f"{domain}/confirm-email/{confirmation_token}"

    background_tasks.add_task(
        send_email,
        to=[new_user.email],
        subject="Por favor confirma tu email",
        template_name="confirmation_email.html",
        template_context={
            "username": new_user.username,
            "confirmation_link": confirmation_link,
        }
    )

    return new_user



@router.get("/confirm-email/{token}")
async def confirm_email(session:DBSession, token:str) -> dict:
    """
    Confirms the user's email address using the provided token. This endpoint
    decodes the email confirmation token to activate the user's account.

    Args:
      - session (DBSession): The database session to use for updating the user.
      - token (str): The token used to confirm the user's email.

    Returns:
      - dict: A message indicating that the user was activated successfully.

    Raises:
      - HTTPException: If the token is invalid or expired, an HTTPException is
          raised with an appropriate error message.
      - HTTPException: If the user is not found, an HTTPException is raised
          with an appropriate error message.
      - HTTPException: If the user is already active, an HTTPException is
          raised an appropriate error message.
    """

    payload = jwt.decode_token(token)
    email = payload.get("sub")

    if not email:
        raise e.InvalidTokenException()

    user = crud.get_user_by_email(session=session, email=email)

    if not user:
        raise e.UserNotFoundException(email)

    if user.status == "active":
        raise e.UserAlreadyRegisteredException(user.email)

    user.status = "active"

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"detail": "Account activation successful!"}



@router.post("/change-password", response_model=UserRead)
async def change_password(
    session:DBSession, current_user:CurrentUser, password_change:PasswordChange
) -> User:
    """
    Changes the user's password. This endpoint allows the current
    authenticated user to change their password.

    Args:
      - session (DBSession): The database session to use for updating the user.
      - current_user (CurrentUser): The current authenticated user object.
      - password_change (PasswordChange): The old and new password data.

    Returns:
      - User: The updated user's details.

    Raises:
      - HTTPException: If the old password is incorrect, an HTTPException is
          raised with an appropriate error message.
      - HTTPException: If the new password is the same as the old password, an
          HTTPException is raised with an appropriate error message.
    """

    if not verify_password(password_change.old_password, current_user.password):
        raise e.OldPasswordException()

    if password_change.old_password == password_change.new_password:
        raise e.NewPasswordException()

    updated_user = crud.change_password(
        session=session,
        user_id=current_user.id,
        new_password=password_change.new_password
    )

    return updated_user



@router.post("/request-password-reset/")
async def request_password_reset(
    session:DBSession,
    request_password_reset:RequestPasswordReset,
    background_tasks:BackgroundTasks,
    request:Request
) -> dict:
    """
    Requests a password reset and sends a reset link to the user's email. This
    endpoint generates a password reset token and sends a reset link to the
    provided email address.

    Args:
      - session (DBSession): The database session to use for retrieving the
          user.
      - request_password_reset (RequestPasswordReset): The email to send a
          reset link.
      - background_tasks (BackgroundTasks): Background tasks to handle sending
          emails.
      - request (Request): The request object provided by FastAPI to access
          information about the incoming request.

    Returns:
      - dict: A message indicating that the password reset link was sent.

    Raises:
      - HTTPException: If the user is not found, an HTTPException is raised
          with an appropriate error message.
    """

    email = request_password_reset.email
    user = crud.get_user_by_email(session=session, email=email)

    if not user:
        raise e.UserNotFoundException(email)

    reset_token = jwt.create_reset_password_token(email)

    domain = f"{request.url.scheme}://{request.headers['host']}"
    reset_link = f"{domain}/reset-password/{reset_token}"

    background_tasks.add_task(
        send_email,
        to=[user.email],
        subject="Solicitud de cambio de contraseña",
        template_name="password_reset_request_email.html",
        template_context={
            "username": user.username,
            "reset_link": reset_link,
        }
    )

    return {"detail": "Password reset link sent!"}



# Arreglar porque el password se está enviando como query param
# GET formulario para establecer contraseña
# POST restablecimiento de contraseña
@router.post("/reset-password/{token}")
async def reset_password(
    session:DBSession, token:str, new_password:str
) -> dict:
    """
    Resets the user's password using the provided token. This endpoint decodes
    the password reset token, verifies it, and updates the user's password.

    Args:
      - session (DBSession): The database session to use for updating the user.
      - token (str): The token used to reset the user's password.
      - new_password (str): The new password to set for the user.

    Returns:
      - dict: A message indicating that the password reset was successful.

    Raises:
      - HTTPException: If the token is invalid or expired, an HTTPException is
          raised with an appropriate error message.
      - HTTPException: If the user is not found, an HTTPException is raised
          with an appropriate error message.
    """

    payload = jwt.decode_token(token)
    email = payload.get("sub")

    if not email:
        raise e.InvalidTokenException()

    user = crud.get_user_by_email(session=session, email=email)

    if not user:
        raise e.UserNotFoundException(email)

    hashed_password = get_password_hash(new_password)
    user.password = hashed_password

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"detail": "Password reset successful!"}
