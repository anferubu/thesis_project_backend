from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, UniqueConstraint

from api.models.utils.base import Base
if TYPE_CHECKING: from api.models.teams import Location, Team



class AgreementTeam(Base, table=True):
    """
    Pivot table between Agreement and Team tables.

    Attributes:
      - agreement_id (int): The ID of the agreement associated with the team.
      - team_id (int): The ID of the team associated with the agreement.

    Constraints:
      - UniqueConstraint on the combination of agreement_id and team_id.
    """

    agreement_id: int = Field(foreign_key="agreement.id")
    team_id: int = Field(foreign_key="team.id")

    __table_args__ = (
        UniqueConstraint("agreement_id", "team_id", name="uq_agreement_team"),
    )



class Agreement(Base, table=True):
    """
    Table for storing the information about club's agreements.

    Attributes:
      - name (str): The name of the agreement.
      - description (str): Description of the agreement (optional).
      - start_date (date): The start date of the agreement.
      - end_date (date): The end date of the agreement.
      - active (bool): Indicates if the agreement is currently active.
      - company_id (int): The ID of the company this agreement is with.

    Relationships:
      - company: Agreement [N:1] Company relationship.
      - teams: Agreement [N:M] Team relationship through AgreementTeam.
    """

    name: str = Field(index=True, unique=True)
    description: str|None = Field(default=None)
    start_date: date
    end_date: date
    active: bool = Field(default=True)
    company_id: int = Field(foreign_key="company.id")

    company: "Company" = Relationship(back_populates="agreements")
    teams: list["Team"] = Relationship(back_populates="agreements", link_model=AgreementTeam)



class Company(Base, table=True):
    """
    Table for storing the information about companies with which the club
    has agreements.

    Attributes:
      - name (str): The name of the company.
      - contact_name (str): The name of the contact person at the company.
      - contact_telephone (str): The telephone number of the contact person.
      - contact_address (str|None): The address of the contact person (optional).

    Relationships:
      - agreements: Company [1:N] Agreement relationship.
    """

    name: str = Field(index=True, unique=True)
    contact_name: str
    contact_telephone: str
    contact_address: str|None = Field(default=None)
    location_id: int = Field(foreign_key="location.id")

    agreements: list[Agreement] = Relationship(back_populates="company")
    location: "Location" = Relationship(back_populates="companies")
