"""
Sets up the database configuration and provides a session dependency for
FastAPI.

It includes:
  - DBSession: Dependency for injecting a database session into endpoints.

(*) To create tables in the database using Alembic:
  1. Create a subclass of SQLModel to represent the table.
  2. Import the class at the end of this file.
  3. Generate a migration script with:
       $ alembic revision --autogenerate -m "<comment>"
  4. Apply the migration to create the table with:
       $ alembic upgrade head

"""

from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine, Session

from core.secrets import env



# Database configuration
DATABASE_URL = env.database_url
engine = create_engine(DATABASE_URL)



def get_db_session() -> Session: # type: ignore
    """
    Return a session from the database.
    """

    with Session(engine) as session:
        yield session


# Dependency: get a session from the database
DBSession = Annotated[Session, Depends(get_db_session)]



# Add all models from api
from api.auth.models import User
from api.roles.models import Role