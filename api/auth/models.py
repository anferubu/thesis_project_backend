"""
Defines the database models for the auth module.

Includes the User table.

"""

from datetime import datetime
from enum import Enum

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel, Relationship

from api.roles.models import Role



class UserStatus(str, Enum):
    """Sets the possible values of the user.status attribute"""

    active = "active"
    inactive = "inactive"
    deleted = "deleted"



class User(SQLModel, table=True):
    """User table"""

    model_config = ConfigDict(strict=True)

    id: int|None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    email: str = Field(unique=True, index=True)
    status: UserStatus = Field(default=UserStatus.inactive)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now)

    role_id: int|None = Field(default=1, foreign_key="role.id")
    role: Role = Relationship()