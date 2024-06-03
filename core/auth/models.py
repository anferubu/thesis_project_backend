from datetime import datetime

from pydantic import ConfigDict, field_validator
from sqlmodel import Field, SQLModel



class User(SQLModel, table=True):
    """User table."""

    model_config = ConfigDict(strict=True)

    id: int|None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    email: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    is_active: bool = False
    is_superuser: bool = False
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now)


    @field_validator("username")
    def username_validation(cls, value:str) -> str:
        if not value.isalnum():
            raise ValueError("username must be alphanumeric")
        if 3 > len(value) > 50:
            raise ValueError("username must contain 3-50 characters.")
        return value


    @field_validator("password")
    def password_validation(cls, value:str) -> str:
        special_characters = "!@#$%^&*()-_=+[]{}|;:'\"<>,.?/~`"

        if len(value) < 8:
            raise ValueError("password be at least 8 characters.")
        if not any(char.islower() for char in value):
            raise ValueError("password must have a lowercase character.")
        if not any(char.isupper() for char in value):
            raise ValueError("password must have a uppercase character.")
        if not any(char.isdigit() for char in value):
            raise ValueError("password must have a numeric character.")
        if not any(char in special_characters for char in value):
            raise ValueError("password must have a special character.")
        return value


    @field_validator("first_name")
    def first_name_validation(cls, value:str) -> str:
        if not all(char.isalpha() or char.isspace() for char in value):
            raise ValueError("first name must be alphabetic.")
        if 1 > len(value) > 50:
            raise ValueError("first name must contain 1-50 characters.")
        return value


    @field_validator("last_name")
    def last_name_validation(cls, value:str) -> str:
        if not all(char.isalpha() or char.isspace() for char in value):
            raise ValueError("last name must be alphabetic.")
        if 1 > len(value) > 50:
            raise ValueError("last name must contain 1-50 characters.")
        return value