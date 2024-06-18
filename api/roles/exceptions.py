"""
Defines the exceptions handler for the roles (and permissions) module.

It includes:
  - RoleNotFoundException
  - PermissionDeniedException
  - RoleAlreadyExistException

"""

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse



class RoleNotFoundException(HTTPException):

    def __init__(self, role_id:int):
        """
        Exception 404 raised when a role is not found in the database.

        Args:
          - role_id (int): The ID of the role that was not found.
        """

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )



class PermissionDeniedException(HTTPException):

    def __init__(self):
        """
        Exception 403 raised when a user tries to access a route without the necessary permissions.
        """

        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User doesn't have the necessary role to access this route"
        )



class RoleAlreadyExistsException(HTTPException):

    def __init__(self, name:str):
        """
        Exception 409 raised when the role is already created. This
        exception is used to indicate that the creation attempt failed because
        the role is already created.

        Args:
          - name (str): The name of the role that is already created.
        """

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Role {name} already exists"
        )
