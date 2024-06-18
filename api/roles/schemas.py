"""
Defines the schemas for the roles (and permissions) module.

Includes:
  - Role schemas: RoleCreate, RoleUpdate, RoleRead.

"""

from sqlmodel import SQLModel



class RoleCreate(SQLModel):
    """Schema for creating a role."""

    name: str
    description: str|None = None



class RoleUpdate(SQLModel):
    """Schema for updating a role."""

    name: str|None = None
    description: str|None = None



class RoleRead(SQLModel):
    """Schema for reading a role."""

    id: int
    name: str
    description: str
