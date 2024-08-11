from datetime import datetime
from typing import Any, Annotated

from pydantic import model_validator
from sqlmodel import create_engine, select, Field, Session, SQLModel

from api.models.users import User
from api.models.utils.enums import EventType
from core.secrets import env



DATABASE_URL = env.database_url
engine = create_engine(DATABASE_URL)



# Event schemas

class EventBase(SQLModel):
    start_date: datetime
    end_date: datetime

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        """Validates the creation/update schema data."""

        # remove whitespaces at beginning and end of a string.
        for key, value in values.items():
            if isinstance(value, str):
                values[key] = value.strip()
        # validate dates
        start_date = values.get("start_date")
        end_date = values.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise ValueError("Start date must be before or equal to end date.")
        return values


class EventCreate(EventBase):
    type: EventType
    name: Annotated[str, Field(min_length=3, max_length=50)]
    description: Annotated[str|None, Field(max_length=1000)] = None
    start_date: datetime
    end_date: datetime
    meeting_point: Annotated[str, Field(max_length=100)]
    location_id: int
    organizer_id: int
    team_id: int
    path_id: int|None = None

    @model_validator(mode="before")
    def validate_organizer_team(cls, values:Any) -> Any:
        """Validates the creation schema data."""

        organizer_id = values.get("organizer_id")
        team_id = values.get("team_id")
        if organizer_id and team_id:
            with Session(engine) as session:
                query = select(User).where(
                    User.profile.id == organizer_id,
                    User.profile.team_id == team_id
                )
                result = session.exec(query).first()
                if result is None:
                    raise ValueError(
                        "The organizer must be a member of the specified team."
                    )
        return values


class EventUpdate(EventBase):
    type: EventType|None = None
    name: Annotated[str|None, Field(min_length=3, max_length=50)] = None
    description: Annotated[str|None, Field(max_length=1000)] = None
    start_date: datetime|None = None
    end_date: datetime|None = None
    meeting_point: Annotated[str|None, Field(max_length=100)] = None
    location_id: int|None = None
    path_id: int|None = None


class EventRead(SQLModel):
    id: int
    type: EventType
    name: str
    description: str|None = None
    start_date: datetime
    end_date: datetime
    meeting_point: str
    location_id: int
    organizer_id: int
    team_id: int
    path_id: int|None = None
    created_at: datetime
    updated_at: datetime


class EventList(SQLModel):
    id: int
    type: EventType
    name: str
    start_date: datetime
    end_date: datetime
    location_id: int



# Participation schemas

class ParticipationCreate(SQLModel):
    attended: bool|None = None


class ParticipationUpdate(SQLModel):
    attended: bool|None = None


class ParticipationRead(SQLModel):
    attended: bool
    member_id: int
    event_id: int
    created_at: datetime
    updated_at: datetime


class ParticipationEventList(SQLModel):
    attended: bool
    event_id: int


class ParticipationMemberList(SQLModel):
    attended: bool
    member_id: int



# Review schemas

class ReviewCreate(SQLModel):
    score: Annotated[int, Field(ge=1, le=5)]
    comment: Annotated[str|None, Field(max_length=500)] = None

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        """Validates the creation/update schema data."""

        # remove whitespaces at beginning and end of a string.
        for key, value in values.items():
            if isinstance(value, str):
                values[key] = value.strip()
        return values


class ReviewUpdate(ReviewCreate):
    score: Annotated[int|None, Field(ge=1, le=5)] = None
    comment: Annotated[str|None, Field(max_length=500)] = None


class ReviewRead(SQLModel):
    score: int
    comment: str
    member_id: int
    event_id: int
    created_at: datetime
    updated_at: datetime


class ReviewEventList(SQLModel):
    score: int
    comment: str
    event_id: int
    created_at: datetime


class ReviewMemberList(SQLModel):
    score: int
    comment: str
    member_id: int
    created_at: datetime



# Path schemas

class PathCreate(SQLModel):
    name: str
    data: str

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        """Validates the creation/update schema data."""

        # remove whitespaces at beginning and end of a string.
        for key, value in values.items():
            if isinstance(value, str):
                values[key] = value.strip()
        return values


class PathUpdate(PathCreate):
    name: str|None = None
    data: str|None = None


class PathRead(SQLModel):
    id: int
    name: str
    data: str
    created_at: datetime
    updated_at: datetime


class PathList(SQLModel):
    id: int
    name: str
