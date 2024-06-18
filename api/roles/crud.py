"""
Defines the CRUD operations for the Role table.

It includes:
  - create_role()
  - get_role_by_id()
  - get_role_by_name()
  - get_roles()
  - update_role()
  - delete_role()

"""

from typing import List
from sqlmodel import Session, select

from api.roles.models import Role
from api.roles.schemas import RoleCreate, RoleUpdate



def create_role(session:Session, role_create:RoleCreate) -> Role:
    """
    Create a new role.

    Args:
      - session (Session): The database session to use for the operation.
      - role_create (RoleCreate): The data for creating the role.

    Returns:
      - Role: The created role.
    """

    new_role = Role.model_validate(role_create)

    session.add(new_role)
    session.commit()
    session.refresh(new_role)

    return new_role



def get_role_by_id(session:Session, role_id:int) -> Role|None:
    """
    Get a role by its ID.

    Args:
      - session (Session): The database session to use for the operation.
      - role_id (int): The ID of the role to retrieve.

    Returns:
      - Role|None: The role with the specified ID, or None if not found.
    """

    return session.get(Role, role_id)



def get_role_by_name(session:Session, name:str) -> Role|None:
    """
    Get a role by its name.

    Args:
      - session (Session): The database session to use for the operation.
      - name (str): The name of the role to retrieve.

    Returns:
      - Role|None: The role with the specified name, or None if not found.
    """

    query = select(Role).where(Role.name == name)
    return session.exec(query).first()



def get_roles(session:Session, skip:int=0, limit:int=10) -> List[Role]:
    """
    Get a list of roles.

    Args:
      - session (Session): The database session to use for the operation.
      - skip (int): The number of roles to skip.
      - limit (int): The maximum number of roles to return.

    Returns:
      - List[Role]: A list of roles.
    """

    query = select(Role).offset(skip).limit(limit)
    return session.exec(query).all()



def update_role(session:Session, role_id:int, role_update:RoleUpdate) -> Role|None:
    """
    Update an existing role.

    Args:
      - session (Session): The database session to use for the operation.
      - role_id (int): The ID of the role to update.
      - role_update (RoleUpdate): The updated role data.

    Returns:
      - Role|None: The updated role, or None if not found.
    """

    role = session.get(Role, role_id)

    if role:
        for field, value in role_update.model_dump(exclude_unset=True).items():
            setattr(role, field, value)

        session.commit()
        session.refresh(role)

    return role



def delete_role(session:Session, role_id:int) -> bool:
    """
    Delete a role by their ID.

    Args:
      - session (Session): The database session to use for the operation.
      - role_id (int): The ID of the role to delete.

    Returns:
      - bool: True if the role was deleted, False otherwise.
    """

    role = session.get(Role, role_id)

    if not role:
        return False

    session.delete(role)
    session.commit()

    return True