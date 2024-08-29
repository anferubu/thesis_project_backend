from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship

from api.models.agreements import Agreement, AgreementTeam
from api.models.utils.base import Base
from api.models.utils.enums import LocationType
if TYPE_CHECKING:
    from api.models.agreements import Company
    from api.models.users import Profile
    from api.models.events import Event



class Team(Base, table=True):
    """Table for storing the information about club's teams.

    Attributes:
      - name (str): The name of the team (unique).
      - location_id (int): The ID of the location where the team is based.

    Relationships:
      - location: Team [N:1] Location relationship.
      - members: Team [1:N] Profile relationship.
      - agreements: Team [N:M] Agreement relationship through AgreementTeam.
      - events: Team [1:N] Event relationship.
    """

    name: str = Field(index=True, unique=True)
    location_id: int = Field(foreign_key="location.id")

    location: "Location" = Relationship(back_populates="team")
    members: list["Profile"] = Relationship(back_populates="team", cascade_delete=True)
    agreements: list["Agreement"] = Relationship(back_populates="teams", link_model=AgreementTeam)
    events: list["Event"] = Relationship(back_populates="team", cascade_delete=True)



class Location(Base, table=True):
    """Table for storing the information about locations (cities and
    departments) of Colombia.

    Only cities have a department_id.

    Attributes:
      - name (str): The name of the location (indexed).
      - type (LocationType): The type of location, e.g., city or department.
      - department_id (int|None): The ID of the department if the location is a city (optional).

    Relationships:
      - department: Location (dept.) [1:N] Location relationship (self-referential).
      - cities: Location [N:1] Location (dept.) relationship (self-referential).
      - team: Location [1:N] Team relationship.
      - events: Location [1:N] Event relationship.
    """

    name: str = Field(index=True)
    type: LocationType
    is_capital: bool|None = Field(default=False)
    department_id: int|None = Field(default=None, foreign_key="location.id")

    department: Optional["Location"] = Relationship(back_populates="cities", sa_relationship_kwargs={"remote_side": "Location.id"})
    cities: list["Location"] = Relationship(back_populates="department")
    team: "Team" = Relationship(back_populates="location")
    events: list["Event"] = Relationship(back_populates="location")
    companies: list["Company"] = Relationship(back_populates="location")
