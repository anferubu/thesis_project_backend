from typing import Optional, TYPE_CHECKING

from pydantic import FilePath
from sqlmodel import Field, Relationship, String, UniqueConstraint

from api.models.utils.base import Base
from api.models.utils.enums import ReactionType, PostStatus
if TYPE_CHECKING: from api.models.users import Profile



class PostTag(Base, table=True):
    """Pivot table between Post and Tag tables.

    Attributes:
      - post_id (int): The ID of the post associated with the tag.
      - tag_id (int): The ID of the tag associated with the post.

    Relationships:
      - post: PostTag [N:1] Post relationship.
      - tag: PostTag [N:1] Tag relationship.

    Constraints:
      - UniqueConstraint on the combination of post_id and tag_id.
    """

    post_id: int = Field(foreign_key="post.id")
    tag_id: int = Field(foreign_key="tag.id")

    __table_args__ = (
        UniqueConstraint("post_id", "tag_id", name="uq_post_tag"),
    )



class Tag(Base, table=True):
    """Table for storing the information about post's tags.

    Attributes:
      - name (str): The name of the tag (unique).

    Relationships:
      - posts: Tag [N:M] Post relationship through PostTag.
    """

    name: str = Field(index=True, unique=True)

    posts: list["Post"] = Relationship(back_populates="tags", link_model=PostTag)



class Post(Base, table=True):
    """Table for storing the information about club's posts.

    Attributes:
      - title (str): The title of the post (unique).
      - slug (str): The URL-safe version of the title.
      - content (str): The content of the post.
      - status (PostStatus): The status of the post, e.g., unpublished, published.
      - thumbnail (FilePath): Thumbnail path.
      - author_id (int): The ID of the author who created the post.

    Relationships:
      - author: Post [N:1] Profile relationship.
      - tags: Post [N:M] Tag relationship through PostTag.
      - comments: Post [1:N] Comment relationship.
    """

    title: str = Field(unique=True)
    slug: str = Field(index=True, unique=True)
    content: str
    status: PostStatus|None = Field(default=PostStatus.UNPUBLISHED)
    thumbnail: FilePath|None = Field(default=None, sa_type=String)
    author_id: int = Field(foreign_key="profile.id")

    author: "Profile" = Relationship(back_populates="posts")
    tags: list[Tag] = Relationship(back_populates="posts", link_model=PostTag)
    comments: list["Comment"] = Relationship(back_populates="post")



class Comment(Base, table=True):
    """Table for storing posts' comments and replies.

    Attributes:
      - content (str): The content of the comment.
      - is_flagged (bool): Indicates if the comment has been reported as inappropriate.
      - author_id (int): The ID of the author who made the comment.
      - post_id (int): The ID of the post being commented on.
      - parent_id (int|None): The ID of the parent comment if this is a reply (optional).

    Relationships:
      - author: Comment [N:1] Profile relationship.
      - post: Comment [N:1] Post relationship.
      - reactions: Comment [1:N] CommentReaction relationship.
      - parent: Comment [1:N] Comment relationship (self-referential, for replies).
      - replies: Comment [1:N] Comment relationship (self-referential, replies to this comment).
    """

    content: str
    is_flagged: bool|None = Field(default=False)
    author_id: int = Field(foreign_key="profile.id")
    post_id: int = Field(foreign_key="post.id")
    parent_id: int|None = Field(default=None, foreign_key="comment.id")

    author: "Profile" = Relationship(back_populates="comments")
    post: Post = Relationship(back_populates="comments")
    reactions: list["CommentReaction"] = Relationship(back_populates="comment")
    parent: Optional["Comment"] = Relationship(back_populates="replies", sa_relationship_kwargs={"remote_side": "Comment.id"})
    replies: list["Comment"] = Relationship(back_populates="parent")



class CommentReaction(Base, table=True):
    """Table for storing interactions (likes and dislikes) on publication's
    comments and replies.

    Attributes:
      - type (ReactionType): The type of reaction, e.g., like or dislike.
      - comment_id (int): The ID of the comment or reply being reacted to.
      - author_id (int): The ID of the author who made the reaction.

    Relationships:
      - comment: CommentReaction [N:1] Comment relationship.
      - author: CommentReaction [N:1] Profile relationship.

    Constraints:
      - UniqueConstraint on the combination of comment_id and author_id.
    """

    type: ReactionType
    comment_id: int = Field(foreign_key="comment.id")
    author_id: int = Field(foreign_key="profile.id")

    comment: Comment = Relationship(back_populates="reactions")
    author: "Profile" = Relationship(back_populates="comment_reactions")

    __table_args__ = (
        UniqueConstraint("comment_id", "author_id", name="uq_comment_author"),
    )
