from datetime import datetime
from typing import Any, Annotated

from pydantic import model_validator
from sqlmodel import Field, SQLModel

from api.models.utils.enums import FeedbackType, FeedbackStatus
from api.schemas import utils



# Feedback schemas

class FeedbackBase(SQLModel):

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        values = utils.remove_whitespaces(values)
        return values


class FeedbackCreate(FeedbackBase):
    type: FeedbackType
    title: Annotated[str, Field(min_length=3, max_length=100)]
    content: Annotated[str, Field(min_length=3, max_length=1000)]
    author_id: int


class FeedbackUpdate(FeedbackBase):
    type: FeedbackType|None = None
    title: Annotated[str|None, Field(min_length=3, max_length=100)] = None
    content: Annotated[str|None, Field(min_length=3, max_length=1000)] = None


class FeedbackRead(SQLModel):
    id: int
    type: FeedbackType
    title: str
    content: str
    author_id: int
    status: FeedbackStatus
    created_at: datetime
    updated_at: datetime


class FeedbackList(SQLModel):
    id: int
    type: FeedbackType
    title: str
    content: str
    author_id: int
    status: FeedbackStatus



# FeedbackAnswer schemas

class FeedbackAnswerBase(SQLModel):

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        values = utils.remove_whitespaces(values)
        return values


class FeedbackAnswerCreate(FeedbackAnswerBase):
    content: Annotated[str, Field(min_length=3, max_length=1000)]
    author_id: int
    feedback_id: int


class FeedbackAnswerUpdate(FeedbackAnswerBase):
    content: Annotated[str|None, Field(min_length=3, max_length=1000)] = None


class FeedbackAnswerRead(SQLModel):
    id: int
    content: str
    author_id: int
    feedback_id: int
    created_at: datetime
    updated_at: datetime


class FeedbackAnswerList(SQLModel):
    id: int
    content: str
    author_id: int
    feedback_id: int
