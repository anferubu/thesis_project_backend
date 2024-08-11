from sqlalchemy import func
from sqlmodel import Session, select

from api.crud.utils import apply_filters, apply_sorting
from api.models.posts import Comment, CommentReaction, Post, Tag
from api.schemas.posts import (
    TagCreate, TagUpdate, PostCreate, PostUpdate, CommentCreate,
    CommentUpdate, CommentReactionCreate, CommentReactionUpdate)



# Tag model CRUD

def create_tag(session:Session, data:TagCreate) -> Tag:
    """Create a tag."""

    new_tag = Tag.model_validate(data)
    session.add(new_tag)
    session.commit()
    session.refresh(new_tag)
    return new_tag



def get_tag_by_id(session:Session, tag_id:int) -> Tag|None:
    """Get a tag by its ID."""

    tag = session.get(Tag, tag_id)
    return tag if tag and not tag.deleted else None



def get_tag_by_name(session:Session, name:str) -> Tag|None:
    """Get a tag by its name."""

    query = select(Tag).where(
        func.lower(Tag.name) == name.lower(), Tag.deleted == False
    )
    return session.exec(query).first()



def list_tags(
    session:Session,
    skip:int|None=None,
    limit:int|None=None,
    sort: dict[str, str]|None = None,
    filter: dict[str, any]|None = None
) -> list[Tag]:
    """List tags."""

    query = select(Tag).where(Tag.deleted == False)
    if filter:
        query = apply_filters(query, Tag, filter)
    if sort:
        query = apply_sorting(query, Tag, sort)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return session.exec(query).all()



def update_tag(
        session:Session, tag_id:int, data:TagUpdate
) -> Tag|None:
    """Update a tag."""

    tag = session.get(Tag, tag_id)
    if tag:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(tag, field, value)
        session.commit()
        session.refresh(tag)
    return tag



def delete_tag(
        session:Session, tag_id:int, hard:bool=False
) -> None:
    """Delete a tag."""

    tag = session.get(Tag, tag_id)
    if tag:
        if hard:
            session.delete(tag)
            session.commit()
        else:
            tag.deleted = True
            session.commit()
            session.refresh(tag)



# Post model CRUD

def create_post(session:Session, data:PostCreate) -> Post:
    """Create a post."""

    post_data = data.model_dump(exclude_unset=True)
    new_post = Post(**post_data)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post



def get_post_by_id(session:Session, post_id:int) -> Post|None:
    """Get a post by its ID."""

    post = session.get(Post, post_id)
    return post if post and not post.deleted else None



def get_post_by_title(session:Session, title:str) -> Post|None:
    """Get a post by its title."""

    query = select(Post).where(
        func.lower(Post.title) == title.lower(), Post.deleted == False
    )
    return session.exec(query).first()



def list_posts(
    session:Session,
    skip:int|None=None,
    limit:int|None=None,
    sort: dict[str, str]|None = None,
    filter: dict[str, any]|None = None
) -> list[Post]:
    """List posts."""

    query = select(Post).where(Post.deleted == False)
    if filter:
        query = apply_filters(query, Post, filter)
    if sort:
        query = apply_sorting(query, Post, sort)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return session.exec(query).all()



def update_post(
        session:Session, post_id:int, data:PostUpdate
) -> Post|None:
    """Update a post."""

    post = session.get(Post, post_id)
    if post:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(post, field, value)
        session.commit()
        session.refresh(post)
    return post



def delete_post(
        session:Session, post_id:int, hard:bool=False
) -> None:
    """Delete a post."""

    post = session.get(Post, post_id)
    if post:
        if hard:
            session.delete(post)
            session.commit()
        else:
            post.deleted = True
            session.commit()
            session.refresh(post)



# Comment model CRUD

def create_comment(session:Session, data:CommentCreate) -> Comment:
    """Create a comment."""

    new_comment = Comment.model_validate(data)
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment



def get_comment_by_id(session:Session, comment_id:int) -> Comment|None:
    """Get a comment by its ID."""

    comment = session.get(Comment, comment_id)
    return comment if comment and not comment.deleted else None



def list_comments(
    session:Session,
    skip:int|None=None,
    limit:int|None=None,
    sort: dict[str, str]|None = None,
    filter: dict[str, any]|None = None
) -> list[Comment]:
    """List comments."""

    query = select(Comment).where(Comment.deleted == False)
    if filter:
        query = apply_filters(query, Comment, filter)
    if sort:
        query = apply_sorting(query, Comment, sort)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return session.exec(query).all()



def update_comment(
        session:Session, comment_id:int, data:CommentUpdate
) -> Comment|None:
    """Update a comment."""

    comment = session.get(Comment, comment_id)
    if comment:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(comment, field, value)
        session.commit()
        session.refresh(comment)
    return comment



def delete_comment(
        session:Session, comment_id:int, hard:bool=False
) -> None:
    """Delete a comment."""

    comment = session.get(Comment, comment_id)
    if comment:
        if hard:
            session.delete(comment)
            session.commit()
        else:
            comment.deleted = True
            session.commit()
            session.refresh(comment)



# CommentReaction model CRUD

def create_reaction(
        session:Session, data:CommentReactionCreate
) -> CommentReaction:
    """Create a reaction."""

    new_reaction = CommentReaction.model_validate(data)
    session.add(new_reaction)
    session.commit()
    session.refresh(new_reaction)
    return new_reaction



def get_reaction_by_id(
        session:Session, reaction_id:int
) -> CommentReaction|None:
    """Get a reaction by its ID."""

    reaction = session.get(CommentReaction, reaction_id)
    return reaction if reaction and not reaction.deleted else None



def list_reactions(
    session:Session,
    skip:int|None=None,
    limit:int|None=None,
    sort: dict[str, str]|None = None,
    filter: dict[str, any]|None = None
) -> list[CommentReaction]:
    """List reactions."""

    query = select(CommentReaction).where(CommentReaction.deleted == False)
    if filter:
        query = apply_filters(query, CommentReaction, filter)
    if sort:
        query = apply_sorting(query, CommentReaction, sort)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return session.exec(query).all()



def update_reaction(
        session:Session, reaction_id:int, data:CommentReactionUpdate
) -> CommentReaction|None:
    """Update a reaction."""

    reaction = session.get(CommentReaction, reaction_id)
    if reaction:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(reaction, field, value)
        session.commit()
        session.refresh(reaction)
    return reaction



def delete_reaction(
        session:Session, reaction_id:int, hard:bool=False
) -> None:
    """Delete a reaction."""

    reaction = session.get(CommentReaction, reaction_id)
    if reaction:
        if hard:
            session.delete(reaction)
            session.commit()
        else:
            reaction.deleted = True
            session.commit()
            session.refresh(reaction)
