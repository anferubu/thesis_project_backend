"""
Define the dependencies used in the roles (and permissions) module.

It includes:
  - AnyRole(): check if the current user has any of the required roles.

"""

from typing import Annotated

from fastapi import Depends

from api.auth.dependencies import CurrentUser
from api.roles import exceptions as e
from api.roles.models import Role



async def get_current_user_role(current_user:CurrentUser) -> Role:
    """
    Get the role of the current user.

    Args:
      - current_user (User): The current authenticated user.

    Returns:
      - Role: The role of the current user.
    """

    return current_user.role


# Dependency: Get the role of the current user
CurrentUserRole = Annotated[Role, Depends(get_current_user_role)]



class RoleChecker:

    def __init__(self, allowed_roles):
        """
        Sets the roles that are allowed to access.
        """

        self.allowed_roles = allowed_roles


    def __call__(self, user_role:CurrentUserRole):
        """
        Evaluates whether the active user has any of the allowed roles.
        """

        if user_role.name not in self.allowed_roles:
            raise e.PermissionDeniedException()

        return True


# Dependency: Check if the current user has any of the specified roles
def check_role(*allowed_roles:str):
    return Depends(RoleChecker(allowed_roles=allowed_roles))