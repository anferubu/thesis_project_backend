"""
Defines the schemas for the auth module.

Includes:
  - Token schemas: Token, TokenPayload.
  - User schemas: UserValidation, UserCreate, UserUpdate, UserRead.
  - Password schemas: PasswordChange

"""

from datetime import datetime

from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel

from api.auth.models import UserStatus



# Token schemas

class Token(SQLModel):
    """Schema for reading the JWT tokens."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"



# User schemas

class UserValidation(SQLModel):
    """Base schema for user validations."""

    username: str
    email: EmailStr
    password: str


    @field_validator("username")
    def username_alphanumeric(cls, value:str) -> str:
        if not value.isalnum():
            raise ValueError("username must be alphanumeric")
        if not (3 <= len(value) <= 50):
            raise ValueError("username must contain 3-50 characters.")
        return value


    @field_validator("email")
    def email_length(cls, value:EmailStr) -> EmailStr:
        if len(value) > 255:
            raise ValueError("email must be less than 255 characters.")
        return value


    @field_validator("password")
    def password_complexity(cls, value: str) -> str:
        special_characters = "!@#$%^&*()-_=+[]{}|;:'\"<>,.?/~`"
        if len(value) < 8:
            raise ValueError("password must be at least 8 characters.")
        if not any(char.islower() for char in value):
            raise ValueError("password must have a lowercase character.")
        if not any(char.isupper() for char in value):
            raise ValueError("password must have an uppercase character.")
        if not any(char.isdigit() for char in value):
            raise ValueError("password must have a numeric character.")
        if not any(char in special_characters for char in value):
            raise ValueError("password must have a special character.")
        return value



class UserCreate(UserValidation):
    """
    Schema for creating a new user.
    you can create a user by setting all fields except id, created_at, updated_at
    """

    username: str
    email: EmailStr
    password: str
    role_id: int
    status: UserStatus|None = None
    is_superuser: bool|None = None



class UserUpdate(UserValidation):
    """
    Schema for updating an existing user.
    You can update any field except id, created_at, updated_at
    """

    username: str|None = None
    email: EmailStr|None = None
    password: str|None = None
    role_id: int|None = None
    status: UserStatus|None = None
    is_superuser: bool|None = None



class UserRead(SQLModel):
    """
    Schema for reading a user.
    Show all fields except password
    """

    id: int
    username: str
    email: EmailStr
    role_id: int
    status: UserStatus
    is_superuser: bool
    created_at: datetime
    updated_at: datetime



# Password Schemas

class PasswordChange(SQLModel):
    """Schema for changing the password"""

    old_password: str
    new_password: str



class RequestPasswordReset(SQLModel):
    """Schema for requesting a password reset email"""
    email: EmailStr
