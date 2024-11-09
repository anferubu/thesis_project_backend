import re
import unicodedata

from datetime import datetime
from typing import Any, Annotated

from pydantic import model_validator, FilePath
from sqlmodel import Field, SQLModel

from api.models.utils.enums import ReactionType, PostStatus
from api.schemas import utils



# Tag schemas

class TagCreate(SQLModel):
    name: Annotated[str, Field(min_length=3, max_length=15)]

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        values = utils.remove_whitespaces(values)
        return values


class TagUpdate(TagCreate):
    name: Annotated[str|None, Field(min_length=3, max_length=15)] = None


class TagRead(SQLModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class TagList(SQLModel):
    id: int
    name: str



# Post schemas

class PostBase(SQLModel):
    title: Annotated[str, Field(min_length=3, max_length=100)]
    slug: str|None = None

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        """Validates the creation/update schema data."""

        values = utils.remove_whitespaces(values)
        # Generate slug if title is present
        if 'title' in values and values['title']:
            values['slug'] = cls.create_slug(values['title'])
        return values


    @classmethod
    def create_slug(cls, title: str) -> str:
        """Generate a slug from the title, handling special characters."""

        # Normalize the title to remove accents and special characters
        normalized_title = unicodedata.normalize('NFKD', title)
        slug = re.sub(r'[^\w\s-]', '', normalized_title)
        slug = slug.lower()
        slug = slug.replace(' ', '-')
        return slug.strip('-')


class PostCreate(PostBase):
    title: Annotated[str, Field(min_length=3, max_length=100)]
    content: Annotated[str, Field(max_length=2500)]
    status: PostStatus|None = None
    thumbnail: FilePath|None = None
    tag_ids: list[int] = []
    author_id: int


class PostUpdate(PostBase):
    title: Annotated[str|None, Field(min_length=3, max_length=100)] = None
    content: Annotated[str|None, Field(max_length=2500)] = None
    status: PostStatus|None = None
    thumbnail: FilePath|None = None


class PostRead(SQLModel):
    id: int
    title: str
    slug: str
    content: str
    tags: list[TagList]
    status: PostStatus
    author_id: int
    thumbnail: FilePath|None = None
    created_at: datetime
    updated_at: datetime


class PostList(SQLModel):
    id: int
    title: str
    tags: list[TagList]
    status: str
    author_id: int


class PaginatedPosts(SQLModel):
    data: list[PostRead]
    pagination: dict



# Comment schemas

class CommentBase(SQLModel):

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        values = utils.remove_whitespaces(values)
        return values


class CommentCreate(CommentBase):
    content: Annotated[str, Field(min_length=3, max_length=500)]
    author_id: int
    post_id: int
    parent_id: int|None = None


class CommentUpdate(CommentBase):
    content: Annotated[str|None, Field(min_length=3, max_length=500)] = None
    is_flagged: bool|None = None


class CommentRead(SQLModel):
    id: int
    content: str
    is_flagged: bool
    author_id: int
    post_id: int
    parent_id: int|None = None
    created_at: datetime
    updated_at: datetime


class CommentList(SQLModel):
    id: int
    content: str
    author_id: int
    post_id: int
    parent_id: int|None = None



# CommentReaction schemas

class CommentReactionCreate(SQLModel):
    type: ReactionType
    comment_id: int
    author_id: int


class CommentReactionUpdate(SQLModel):
    type: ReactionType|None


class CommentReactionRead(SQLModel):
    id: int
    type: ReactionType
    comment_id: int
    author_id: int
    created_at: datetime
    updated_at: datetime


class CommentReactionList(SQLModel):
    id: int
    type: ReactionType
    comment_id: int
    author_id: int
