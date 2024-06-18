"""
Defines the database models for the roles (and permissions) module.

Includes the Role table.

"""

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel



class Role(SQLModel, table=True):
    """Role table."""

    model_config = ConfigDict(strict=True)

    id: int|None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: str|None = None
