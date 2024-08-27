from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, UniqueConstraint

from api.models.utils.base import Base
from api.models.utils.enums import EventType
if TYPE_CHECKING:
    from api.models.users import Profile
    from api.models.teams import Location, Team



class Event(Base, table=True):
    """Table for storing the information about club's events.

    Attributes:
      - type (EventType): The type of the event, e.g., ride, meeting, etc.
      - name (str): The name of the event.
      - description (str): Description of the event (optional).
      - start_date (datetime): The start date and time of the event.
      - end_date (datetime): The end date and time of the event.
      - meeting_point (str): The meeting point for the event (optional).
      - location_id (int): The ID of the location where the event takes place.
      - organizer_id (int): The ID of the member organizing the event.
      - team_id (int): The ID of the team associated with the event.
      - path_id (int): The ID of the path related to the event (optional).

    Relationships:
      - location: Event [N:1] Location relationship.
      - organizer: Event [N:1] Profile relationship (organizer).
      - team: Event [N:1] Team relationship.
      - path: Event [N:1] Path relationship.
      - reviews: Event [1:N] Review relationship.
      - members: Event [1:N] Participation relationship.
    """

    type: EventType = Field(default=EventType.RIDE)
    name: str
    description: str|None = Field(default=None)
    start_date: datetime
    end_date: datetime
    meeting_point: str|None = Field(default=None)
    location_id: int = Field(foreign_key="location.id")
    organizer_id: int = Field(foreign_key="profile.id")
    team_id: int = Field(foreign_key="team.id")
    path_id: int|None = Field(default=None, foreign_key="path.id")

    location: "Location" = Relationship(back_populates="events")
    organizer: "Profile" = Relationship(back_populates="organized_events")
    team: "Team" = Relationship(back_populates="events")
    path: "Path" = Relationship(back_populates="events")
    reviews: list["Review"] = Relationship(back_populates="event", cascade_delete=True)
    members: list["Participation"] = Relationship(back_populates="event", cascade_delete=True)



class Participation(Base, table=True):
    """Table for storing the information about event's participations.
    This model is a pivot table between Event and Profile tables.

    Any user can confirm attendance, but only those who actually attended the
    event will have the field attend=True.

    Attributes:
      - attended (bool): Indicates if the member attended the event.
      - member_id (int): The ID of the member participating in the event.
      - event_id (int): The ID of the event the member participated in.

    Relationships:
      - member: Participation [N:1] Profile relationship.
      - event: Participation [N:1] Event relationship.

    Constraints:
      - UniqueConstraint on the combination of member_id and event_id.
    """

    attended: bool|None = Field(default=False)
    member_id: int = Field(foreign_key="profile.id")
    event_id: int = Field(foreign_key="event.id")

    member: "Profile" = Relationship(back_populates="attended_events")
    event: Event = Relationship(back_populates="members")

    __table_args__ = (
        UniqueConstraint("member_id", "event_id", name="uq_participation_member_event"),
    )



class Review(Base, table=True):
    """Table for storing the information about event's reviews.
    This model is a pivot table between Event and Profile tables.

    Attributes:
      - score (int): The rating score given by the member.
      - comment (str): The review comment provided by the member (optional).
      - author_id (int): The ID of the member who wrote the review.
      - event_id (int): The ID of the event being reviewed.

    Relationships:
      - author: Review [N:1] Profile relationship.
      - event: Review [N:1] Event relationship.

    Constraints:
      - UniqueConstraint on the combination of author_id and event_id.
    """

    score: int
    comment: str|None = Field(default=None)
    author_id: int = Field(foreign_key="profile.id")
    event_id: int = Field(foreign_key="event.id")

    author: "Profile" = Relationship(back_populates="reviews")
    event: "Event" = Relationship(back_populates="reviews")

    __table_args__ = (
        UniqueConstraint("author_id", "event_id", name="uq_review_author_event"),
    )



class Path(Base, table=True):
    """Table for storing the information about event's paths.

    Attributes:
      - name (str): The name of the path (unique).
      - data (str): Data describing the path, e.g., coordinates.

    Relationships:
      - events: Path [1:N] Event relationship.
    """

    name: str = Field(index=True, unique=True)
    data: str

    events: list[Event] = Relationship(back_populates="path")
