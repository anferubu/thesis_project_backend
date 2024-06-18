"""
Define the endpoints for the roles (and permissions) module.

Includes:
  - GET /roles
  - GET /roles/{role_id}
  - POST /roles
  - PUT /roles/{role_id}
  - DELETE /roles/{role_id}

"""

from typing import List

from fastapi import APIRouter, status

from api.roles import crud, exceptions as e
from api.roles.dependencies import check_role
from api.roles.models import Role
from api.roles.schemas import RoleRead, RoleCreate, RoleUpdate
from core.database import DBSession



router = APIRouter()


@router.get(
    "/roles",
    response_model=List[RoleRead],
    dependencies=[check_role("admin")]
)
async def list_roles(
    session:DBSession,
    skip:int=0,
    limit:int=10
) -> List[Role]:
    """
    Retrieve a list of roles with pagination.

    Args:
      - session (DBSession): The database session to use for the query.
      - skip (int): The number of records to skip (default is 0).
      - limit (int): The maximum number of records to return (default is 10).

    Returns:
      - List[Role]: A list of roles.
    """

    return crud.get_roles(session=session, skip=skip, limit=limit)



@router.post(
    "/roles",
    response_model=RoleRead,
    status_code=status.HTTP_201_CREATED
)
async def create_role(session:DBSession, role_in:RoleCreate) -> Role:
    """
    Create a new role.

    Args:
      - session (DBSession): The database session to use for the query.
      - role_in (RoleCreate): The data for the new role.

    Returns:
        Role: The created role.
    """

    existing_role = crud.get_role_by_name(session=session, name=role_in.name)

    if existing_role:
        raise e.RoleAlreadyExistsException(role_in.name)

    return crud.create_role(session=session, role_create=role_in)



@router.get(
    "/roles/{role_id}",
    response_model=RoleRead,
)
async def get_role(session:DBSession, role_id:int) -> Role:
    """
    Retrieve a role by its ID.

    Args:
      - session (DBSession): The database session to use for the query.
      - role_id (int): The ID of the role to retrieve.

    Returns:
      - Role: The role with the specified ID.

    Raises:
      - HTTPException: If the role is not found, raises an error.
    """

    role = crud.get_role_by_id(session=session, role_id=role_id)

    if not role:
        raise e.RoleNotFoundException(role_id)

    return role



@router.put(
    "/roles/{role_id}",
    response_model=RoleRead,
)
async def update_role(session:DBSession, role_id:int, role_in:RoleUpdate) -> Role:
    """
    Update a role by its ID.

    Args:
      - session (DBSession): The database session to use for the query.
      - role_id (int): The ID of the role to update.
      - role_in (RoleUpdate): The data to update the role with.

    Returns:
      - Role: The updated role.

    Raises:
      - HTTPException: If the role is not found, raises an error.
    """

    role = crud.update_role(
        session=session,
        role_id=role_id,
        role_update=role_in
    )

    if not role:
        raise e.RoleNotFoundException(role_id)

    return role



@router.delete(
    "/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_role(session:DBSession, role_id:int) -> None:
    """
    Delete a role by its ID.

    Args:
      - session (DBSession): The database session to use for the query.
      - role_id (int): The ID of the role to delete.

    Raises:
      - HTTPException: If the role is not found, raises an error.
    """

    role = crud.get_role_by_id(session=session, role_id=role_id)

    if not role:
        raise e.RoleNotFoundException(role_id)

    crud.delete_role(session=session, role_id=role_id)
