from datetime import datetime
from typing import Any, Annotated

from pydantic import model_validator
from sqlmodel import Field, SQLModel

from api.models.utils.enums import LocationType
from api.schemas import utils



# Team schemas

class TeamBase(SQLModel):

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        values = utils.remove_whitespaces(values)
        return values


class TeamCreate(TeamBase):
    name: Annotated[str, Field(min_length=3, max_length=50)]
    location_id: int


class TeamUpdate(TeamBase):
    name: Annotated[str|None, Field(min_length=3, max_length=50)] = None


class TeamRead(SQLModel):
    id: int
    name: str
    location_id: int
    created_at: datetime
    updated_at: datetime


class TeamList(SQLModel):
    id: int
    name: str
    location_id: int


class TeamAdd(SQLModel):
    id: int



# Location schemas

class LocationBase(SQLModel):

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        values = utils.remove_whitespaces(values)
        return values


class LocationCreate(LocationBase):
    name: Annotated[str, Field(min_length=3, max_length=50)]
    type: LocationType
    is_capital: bool = False
    department_id: int|None = None


class LocationUpdate(LocationBase):
    name: Annotated[str|None, Field(min_length=3, max_length=50)] = None
    type: LocationType|None = None
    is_capital: bool|None = None
    department_id: int|None = None


class LocationRead(SQLModel):
    id: int
    name: str
    type: LocationType
    is_capital: bool
    department_id: int|None = None
    created_at: datetime
    updated_at: datetime


class LocationList(SQLModel):
    id: int
    name: str
    type: LocationType
    is_capital: bool
    department_id: int|None = None
