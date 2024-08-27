from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from api.models.utils.base import Base
from api.models.utils.enums import FeedbackType, FeedbackStatus
if TYPE_CHECKING: from api.models.users import Profile



class Feedback(Base, table=True):
    """Table for storing the information about club's feedback (questions,
    suggestions, and complaints).

    Attributes:
      - type (FeedbackType): The type of feedback, e.g., question, suggestion, complaint.
      - title (str): The title of the feedback.
      - content (str): The content of the feedback.
      - status (FeedbackStatus): The status of the feedback, e.g., pending, resolved.
      - author_id (int): The ID of the author who submitted the feedback.

    Relationships:
      - author: Feedback [N:1] Profile relationship.
      - answer: Feedback [1:1] FeedbackAnswer relationship.
    """

    type: FeedbackType
    title: str
    content: str
    status: FeedbackStatus|None = Field(default=FeedbackStatus.PENDING)
    author_id: int = Field(foreign_key="profile.id")

    author: "Profile" = Relationship(back_populates="feedbacks")
    answer: "FeedbackAnswer" = Relationship(back_populates="feedback", sa_relationship_kwargs={"uselist": False}, cascade_delete=True)



class FeedbackAnswer(Base, table=True):
    """Table for storing feedback's answers.

    Attributes:
      - content (str): The content of the answer to the feedback.
      - author_id (int): The ID of the author who provided the answer.
      - feedback_id (int): The ID of the feedback being answered (unique).

    Relationships:
      - author: FeedbackAnswer [N:1] Profile relationship.
      - feedback: FeedbackAnswer [1:1] Feedback relationship.
    """

    content: str
    author_id: int = Field(foreign_key="profile.id")
    feedback_id: int = Field(foreign_key="feedback.id", unique=True)

    author: "Profile" = Relationship(back_populates="feedback_answers")
    feedback: "Feedback" = Relationship(back_populates="answer", sa_relationship_kwargs={"uselist": False})
