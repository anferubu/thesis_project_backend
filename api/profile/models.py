"""
Defines the database models for the profile module.

Includes the Profile table.

"""

from datetime import datetime

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel, Relationship

from api.auth.models import User



class Profile(SQLModel, table=True):
    """Profile table."""

    model_config = ConfigDict(strict=True)

    id: int|None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    phone: str
    status: str
    document_type: str
    document_number: str
    rh: str
    birthdate: datetime
    genre: str
    avatar: str
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now)

    user_id: int|None = Field(default=None, foreign_key="user.id")
    user: User = Relationship()

    #city_id: int|None = Field(default=None, foreign_key="city.id")
    #city: City = Relationship()

    #team_id: int|None = Field(default=None, foreign_key="team.id")
    #team: Team = Relationship()
