from fastapi import APIRouter, BackgroundTasks, HTTPException, Request

from api.crud import users as crud
from api.dependencies.auth import CurrentUser, LoginFormData
from api.models.users import User
from api.schemas.users import (
    PasswordChange, Token, TokenRefreshRequest, UserCreate, UserRead,
    RequestPasswordReset)
from api.utils.security import jwt
from api.utils.security.authenticate import authenticate
from api.utils.security.hashing import verify_password, get_password_hash
from core.database import DBSession
from core.email import send_email



auth = APIRouter()



@auth.post("/token", response_model=Token)
def login_for_access_token(
    session:DBSession, form_data:LoginFormData
) -> Token:
    """Authenticate the user and provide an access token and a refresh token."""

    user = authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(401, "Incorrect credentials!")
    elif user.status == "inactive":
        raise HTTPException(403, f"User with email {user.email} is inactive!")
    return Token(
        access_token=jwt.create_access_token(user.email),
        refresh_token=jwt.create_refresh_token(user.email)
    )



@auth.post("/refresh-token", response_model=Token)
def refresh_access_token(data:TokenRefreshRequest) -> Token:
    """Refreshes the access token using the provided refresh token. """

    payload = jwt.decode_token(data.refresh_token)
    email = payload.get("sub")
    if not email:
        raise HTTPException(401, "Invalid or expired token!")
    return Token(
        access_token=jwt.create_access_token(email),
        refresh_token=jwt.create_refresh_token(email)
    )



@auth.get("/users/me", response_model=UserRead)
def read_user_me(current_user:CurrentUser) -> User:
    """Retrieves the current authenticated user's information."""

    return current_user



@auth.post("/register", response_model=UserRead)
def register_user(
    session:DBSession,
    data:UserCreate,
    background_tasks:BackgroundTasks,
    request:Request
) -> User:
    """Registers a new user and sends a confirmation email."""

    user = crud.get_user_by_email(session, data.email)
    if user:
        raise HTTPException(409, f"User {user.email} is already registered!")
    new_user = crud.create_user(session, data)
    confirmation_token = jwt.create_confirmation_token(new_user.email)
    domain = f"{request.url.scheme}://{request.headers['host']}"
    confirmation_link = f"{domain}/confirm-email/{confirmation_token}"
    background_tasks.add_task(
        send_email,
        to=[new_user.email],
        subject="Por favor confirma tu email",
        template_name="confirmation_email.html",
        template_context={
            "fullname": f"{new_user.profile.first_name} {new_user.profile.last_name}",
            "confirmation_link": confirmation_link,
        }
    )
    return new_user



@auth.get("/confirm-email/{token}")
def confirm_email(session:DBSession, token:str) -> dict:
    """Confirms the user's email address using the provided token. This
    endpointdecodes the email confirmation token to activate the user's
    account."""

    payload = jwt.decode_token(token)
    email = payload.get("sub")
    if not email:
        raise HTTPException(401, "Invalid or expired token!")
    user = crud.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(404, f"User with email {email} not found")
    if user.status == "active":
        raise HTTPException(
            409, f"User with email {user.email} is already registered!"
        )
    user.status = "active"
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"detail": "Account activation successful!"}



@auth.post("/change-password", response_model=UserRead)
def change_password(
    session:DBSession, current_user:CurrentUser, password_change:PasswordChange
) -> User:
    """Changes the user's password. This endpoint allows the current
    authenticated user to change their password."""

    if not verify_password(password_change.old_password, current_user.password):
        raise HTTPException(400, "Old password is incorrect!")
    if password_change.old_password == password_change.new_password:
        raise HTTPException(400, "New password cannot be the same as the old password.")
    updated_user = crud.change_password(
        session=session,
        user_id=current_user.id,
        new_password=password_change.new_password
    )
    return updated_user



@auth.post("/request-password-reset/")
def request_password_reset(
    session:DBSession,
    request_password_reset:RequestPasswordReset,
    background_tasks:BackgroundTasks,
    request:Request
) -> dict:
    """Requests a password reset and sends a reset link to the user's email.
    This endpoint generates a password reset token and sends a reset link to
    the provided email address."""

    email = request_password_reset.email
    user = crud.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(404, f"User with email {email} not found")
    reset_token = jwt.create_reset_password_token(email)
    domain = f"{request.url.scheme}://{request.headers['host']}"
    reset_link = f"{domain}/reset-password/{reset_token}"
    background_tasks.add_task(
        send_email,
        to=[user.email],
        subject="Solicitud de cambio de contraseña",
        template_name="password_reset_request_email.html",
        template_context={
            "fullname": f"{user.profile.first_name} {user.profile.last_name}",
            "reset_link": reset_link,
        }
    )
    return {"detail": "Password reset link sent!"}



# Arreglar porque el password se está enviando como query param
# GET formulario para establecer contraseña
# POST restablecimiento de contraseña
@auth.post("/reset-password/{token}")
def reset_password(
    session:DBSession, token:str, new_password:str
) -> dict:
    """Resets the user's password using the provided token. This endpoint
    decodes the password reset token, verifies it, and updates the user's
    password."""

    payload = jwt.decode_token(token)
    email = payload.get("sub")
    if not email:
        raise HTTPException(401, "Invalid or expired token!")
    user = crud.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(404, f"User with email {email} not found")
    hashed_password = get_password_hash(new_password)
    user.password = hashed_password
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"detail": "Password reset successful!"}
