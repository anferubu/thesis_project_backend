from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.logging import LogRequestsMiddleware
from core.secrets import env



# Application description
DEBUG = env.app_debug

description = """
Description here...
"""

app = FastAPI(
    debug=env.app_debug,
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
app.add_middleware(LogRequestsMiddleware)


# Routes added
from core.auth.routers import auth

app.include_router(auth)


# Directories definition
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_FILES_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
EMAIL_TEMPLATES_DIR = TEMPLATES_DIR / "email"


# Static File (Images, JS, CSS)
app.mount(
    "/static",
    StaticFiles(directory=STATIC_FILES_DIR),
    name="static"
)


# Templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)