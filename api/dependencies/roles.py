from typing import Annotated

from fastapi import Depends, HTTPException

from api.dependencies.auth import CurrentUser
from api.models.users import Role



async def get_current_user_role(current_user:CurrentUser) -> Role:
    """Get the role of the current (authenticated) user."""

    return current_user.role


# Dependency: Get the role of the current user
CurrentUserRole = Annotated[Role, Depends(get_current_user_role)]



class RoleChecker:

    def __init__(self, allowed_roles):
        """Sets the roles that are allowed to access."""

        self.allowed_roles = allowed_roles


    def __call__(self, user_role:CurrentUserRole):
        """Evaluates whether the active user has any of the allowed roles."""

        print("USER ROL ID", user_role.id)
        print("ALLOWED ROLES", self.allowed_roles)

        if user_role.id not in self.allowed_roles:
            raise HTTPException(
                403,
                "You are not authorized to access this resource."
            )
        return True


# Dependency: Check if the current user has any of the specified roles
def roles_required(*allowed_roles:str):
    return Depends(RoleChecker(allowed_roles=allowed_roles))
