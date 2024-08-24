"""
Sets the FastAPI application settings.

It sets up the application with necessary configurations, middleware, static
files, templates, and routes.

(*) Add a description for the API.

"""

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.routers import router
from core.secrets import env



description = """
This API is designed to manage the comprehensive information of a motorcycle
club, including member details, event planning, and various other related
activities. The API ensures secure access and data integrity through robust
authentication and authorization mechanisms, making it an essential tool for
the smooth operation of motorcycle clubs.

This API aims to streamline the administrative tasks of motorcycle clubs,
allowing them to focus more on their passion for riding and community building.
"""

DEBUG = env.app_debug
BASE_DIR = Path(__file__).resolve().parent.parent


# API definition
app = FastAPI(
    debug=DEBUG,
    title=env.app_name,
    summary=f"{env.app_name} API",
    description=description,
    version=env.app_version,
    redoc_url=None,
)

app.docs_url = None if not DEBUG else "/docs"


# Middlewares added
app.add_middleware(
    CORSMiddleware,
    allow_origins=env.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Routes added
app.include_router(router)


# Static File (Images, JS, CSS) settings
STATIC_FILES_DIR = BASE_DIR / "static"

app.mount(
    "/static",
    StaticFiles(directory=STATIC_FILES_DIR),
    name="static"
)


# Templates settings
TEMPLATES_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=TEMPLATES_DIR)


# Remove warnings from passlib module
logging.getLogger('passlib').setLevel(logging.ERROR)
