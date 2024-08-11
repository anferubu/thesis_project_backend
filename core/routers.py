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
from api.routers.agreements import agreement, company
from api.routers.events import event, participation, review, path



router = APIRouter()

router.include_router(agreement, tags=["agreements"])
router.include_router(company, tags=["companies"])
router.include_router(event, tags=["events"])
router.include_router(participation, tags=["participations"])
router.include_router(review, tags=["reviews"])
router.include_router(path, tags=["paths"])
