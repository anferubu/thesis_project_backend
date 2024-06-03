from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from core.database.db import engine



def get_db_session() -> Session: # type: ignore
    """
    Return a session from the database.
    """

    with Session(engine) as session:
        yield session


DBSession = Annotated[Session, Depends(get_db_session)]
