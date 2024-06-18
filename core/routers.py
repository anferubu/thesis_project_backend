"""
Groups all APIRouter of the application.

It serves as the central place to include all the routers from various modules
that make up the API. To extend the API, import the routers from the respective
modules and include them here.

Usage:
1. Import routers from other modules.
2. Include those routers using `router.include_router()`.

Example:
from app_module.router import module_router
router.include_router(module_router, prefix="/module", tags=["Module"])

"""

from fastapi import APIRouter

# Add all routers from apps
from api.auth.routers import router as auth_router
from api.roles.routers import router as roles_router



router = APIRouter()

router.include_router(auth_router, prefix="", tags=["auth"])
router.include_router(roles_router, prefix="", tags=["roles"])
