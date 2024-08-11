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
from api.routers.auth import auth
from api.routers.chatbot import chat
from api.routers.events import event, participation, review, path
from api.routers.feedbacks import feedback, answer
from api.routers.posts import tag, post, comment, reaction
from api.routers.teams import team, location
from api.routers.users import (role, user, motorcycle, brand,
    membership, birthdate)



router = APIRouter()


router.include_router(agreement, tags=["Agreements"])
router.include_router(chat, tags=["AI assistant"])
router.include_router(answer, tags=["Answers of feedbacks"])
router.include_router(auth, tags=["Authentication"])
router.include_router(brand, tags=["Brands of motorcycles"])
router.include_router(birthdate, tags=["Birthdates of users"])
router.include_router(comment, tags=["Comments of posts"])
router.include_router(company, tags=["Companies of the agreements"])
router.include_router(event, tags=["Events of the motorcycle's club"])
router.include_router(feedback, tags=["Feedbacks"])
router.include_router(location, tags=["Locations of Colombia"])
router.include_router(membership, tags=["Membership card of the club"])
router.include_router(motorcycle, tags=["Motorcycles of users"])
router.include_router(participation, tags=["Participations of an event"])
router.include_router(path, tags=["Paths of an event"])
router.include_router(post, tags=["Posts"])
router.include_router(reaction, tags=["Reactions of comments"])
router.include_router(review, tags=["Reviews of an event"])
router.include_router(role, tags=["Roles of users"])
router.include_router(tag, tags=["Tags of posts"])
router.include_router(team, tags=["Teams of the motorcycle's club"])
router.include_router(user, tags=["Users of the motorcycle's club"])
