from datetime import date
from typing import TYPE_CHECKING

from pydantic import FilePath
from sqlmodel import Field, Relationship, String

from api.models.utils.base import Base
from api.models.utils.enums import UserStatus, DocumentType, GenderType, RHType
if TYPE_CHECKING:
    from api.models.events import Event, Participation, Review
    from api.models.feedbacks import Feedback, FeedbackAnswer
    from api.models.posts import Comment, CommentReaction,  Post
    from api.models.teams import Team



class Role(Base, table=True):
    """Role table.

    Attributes:
      - name (str): The name of the role (unique).
      - description (str|None): A description of the role (optional).

    Relationships:
      - users: Role [1:N] User relationship.
    """

    name: str = Field(index=True, unique=True)
    description: str|None = Field(default=None)

    users: list["User"] = Relationship(back_populates="role", cascade_delete=True)



class User(Base, table=True):
    """Table for storing the information about club's users.
    This table contains the authentication information.

    Attributes:
      - email (str): The email address of the user (unique).
      - password (str): The password of the user.
      - status (UserStatus): The status of the user, e.g., active or inactive.
      - role_id (int): The ID of the role assigned to the user (default is 1).

    Relationships:
      - role: User [N:1] Role relationship.
      - member: User [1:1] Profile relationship.
    """

    email: str = Field(index=True, unique=True)
    password: str
    status: UserStatus|None = Field(default=UserStatus.INACTIVE)
    role_id: int|None = Field(default=1, foreign_key="role.id")

    role: "Role" = Relationship(back_populates="users")
    profile: "Profile" = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False}, cascade_delete=True)



class Profile(Base, table=True):
    """Table for storing the information about club's users.
    This table contains the profile information.

    Attributes:
      - first_name (str): The first name of the member.
      - last_name (str): The last name of the member.
      - nickname (str|None): The nickname of the member (optional).
      - telephone (str|None): The telephone number of the member (optional).
      - document_type (DocumentType): The type of document used for identification.
      - document_number (str): The identification number on the document.
      - rh (RHType): The blood type of the member.
      - birthdate (date): The birthdate of the member.
      - genre (GenderType): The gender of the member.
      - photo (FilePath|None): The path to the member's photo (optional).
      - user_id (int): The ID of the user account associated with the member.
      - team_id (int): The ID of the team the member is part of.

    Relationships:
      - user: Profile [1:1] User relationship.
      - team: Profile [N:1] Team relationship.
      - motorcycles: Profile [1:N] Motorcycle relationship.
      - attended_events: Profile [1:N] Participation relationship.
      - organized_events: Profile [1:N] Event relationship.
      - reviews: Profile [1:N] Review relationship.
      - posts: Profile [1:N] Post relationship.
      - comments: Profile [1:N] Comment relationship.
      - comment_reactions: Profile [1:N] CommentReaction relationship.
      - feedbacks: Profile [1:N] Feedback relationship.
      - feedback_answers: Profile [1:N] FeedbackAnswer relationship.
    """

    first_name: str
    last_name: str
    nickname: str|None = Field(default=None)
    telephone: str|None = Field(default=None)
    document_type: DocumentType
    document_number: str
    rh: RHType
    birthdate: date
    genre: GenderType
    # When using StrClass|None, sa_type=String must be specified
    photo: FilePath|None = Field(default=None, sa_type=String)
    user_id: int = Field(foreign_key="user.id")
    team_id: int = Field(foreign_key="team.id")

    user: User = Relationship(back_populates="profile", sa_relationship_kwargs={"uselist": False})
    team: "Team" = Relationship(back_populates="members")
    motorcycles: list["Motorcycle"] = Relationship(back_populates="owner", cascade_delete=True)
    attended_events: list["Participation"] = Relationship(back_populates="member", cascade_delete=True)
    organized_events: list["Event"] = Relationship(back_populates="organizer", cascade_delete=True)
    reviews: list["Review"] = Relationship(back_populates="author", cascade_delete=True)
    posts: list["Post"] = Relationship(back_populates="author", cascade_delete=True)
    comments: list["Comment"] = Relationship(back_populates="author", cascade_delete=True)
    comment_reactions: list["CommentReaction"] = Relationship(back_populates="author", cascade_delete=True)
    feedbacks: list["Feedback"] = Relationship(back_populates="author", cascade_delete=True)
    feedback_answers: list["FeedbackAnswer"] = Relationship(back_populates="author", cascade_delete=True)



class Motorcycle(Base, table=True):
    """Table for storing the information about club's motorcycles.

    Attributes:
      - model (str): The model of the motorcycle.
      - license_plate (str): The license plate of the motorcycle.
      - photo (FilePath|None): The path to the motorcycle's photo (optional).
      - brand_id (int): The ID of the brand associated with the motorcycle.
      - owner_id (int): The ID of the member who owns the motorcycle.

    Relationships:
      - brand: Motorcycle [N:1] Brand relationship.
      - owner: Motorcycle [N:1] Profile relationship.
    """

    model: str
    license_plate: str
    photo: FilePath|None = Field(default=None, sa_type=String)
    brand_id: int = Field(foreign_key="brand.id")
    owner_id: int = Field(foreign_key="profile.id")

    brand: "Brand" = Relationship(back_populates="motorcycles")
    owner: "Profile" = Relationship(back_populates="motorcycles")



class Brand(Base, table=True):
    """Table for storing the information about motorcycle's brands.

    Attributes:
      - name (str): The name of the brand (unique).

    Relationships:
      - motorcycles: Brand [1:N] Motorcycle relationship.
    """

    name: str = Field(index=True, unique=True)

    motorcycles: list[Motorcycle] = Relationship(back_populates="brand", cascade_delete=True)
