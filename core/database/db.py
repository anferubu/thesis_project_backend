from sqlmodel import create_engine

from core.secrets import env



# Database configuration
DATABASE_URL = env.database_url
DEBUG = env.app_debug

engine = create_engine(DATABASE_URL, echo=DEBUG)



# Add all models from api
from core.auth.models import User