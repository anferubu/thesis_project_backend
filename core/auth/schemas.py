from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, SQLModel



class Token(SQLModel):
    """Schema for reading an access token."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    """Schema for the payload within the JWT access token."""

    email: str|None = None



class UserBase(SQLModel):
    """Base schema for User."""

    username: str
    email: EmailStr = Field(unique=True, index=True)
    first_name: str
    last_name: str
    is_active: bool = False
    is_superuser: bool = False


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str


class UserUpdate(SQLModel):
    """Schema for updating an existing user."""

    username: str|None = None
    email: EmailStr|None = None
    first_name: str|None = None
    last_name: str|None = None
    password: str|None = None
    is_active: bool|None = None
    is_superuser: bool|None = None


class UserRead(UserBase):
    """Schema for reading a user."""

    id: int
    created_at: datetime
    updated_at: datetime