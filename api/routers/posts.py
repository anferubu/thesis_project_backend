from fastapi import APIRouter, HTTPException

from api.crud import posts as crud
from api.crud.users import get_user_by_id
from api.crud.utils import parse_filter_param, parse_sort_param
from api.models.posts import Post, Tag, Comment, CommentReaction
from api.schemas.posts import (
    PostCreate, PostRead, PostUpdate, PostList, TagCreate, TagRead, TagUpdate,
    TagList, CommentCreate, CommentRead, CommentUpdate, CommentList,
    CommentReactionCreate, CommentReactionRead, CommentReactionUpdate,
    CommentReactionList)
from api.schemas.users import UserRead
from core.database import DBSession as Session



tag = APIRouter()



# Tag endpoints

@tag.get("/tags", response_model=list[TagList])
def list_tags(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> list[Tag]:
    """List tags."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    return crud.list_tags(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )



@tag.post("/tags", response_model=TagRead, status_code=201)
def create_tag(session:Session, data:TagCreate) -> Tag:
    """Create a new tag."""

    tag = crud.get_tag_by_name(session, data.name)
    if tag:
        raise HTTPException(409, f"Tag {data.name} already exists!")
    return crud.create_tag(session, data)



@tag.get("/tags/{tag_id}", response_model=TagRead)
def get_tag(session:Session, tag_id:int) -> Tag:
    """Get a tag by its ID."""

    tag = crud.get_tag_by_id(session, tag_id)
    if not tag:
        raise HTTPException(404, f"Tag #{tag_id} not found!")
    return tag



@tag.put("/tags/{tag_id}", response_model=TagRead)
def update_tag(
    session:Session, tag_id:int, data:TagUpdate
) -> Tag:
    """Update a tag."""

    tag = crud.update_tag(session, tag_id, data)
    if not tag:
        raise HTTPException(404, f"Tag #{tag_id} not found!")
    return tag



@tag.delete("/tags/{tag_id}", status_code=204)
def delete_tag(
    session:Session, tag_id:int, hard:bool=False
) -> None:
    """Delete a tag by its ID."""

    tag = crud.get_tag_by_id(session, tag_id)
    if not tag:
        raise HTTPException(404, f"Tag #{tag_id} not found!")
    crud.delete_tag(session, tag_id, hard)



# Tag relationship endpoints

@tag.get("/tags/{tag_id}/posts", response_model=list[PostList])
def list_tag_posts(session:Session, tag_id:int):
    """Get the posts with a tag."""

    tag = crud.get_tag_by_id(session, tag_id)
    if not tag:
        raise HTTPException(404, f"Tag #{tag_id} not found!")
    return tag.posts



# Post endpoints

post = APIRouter()

@post.get("/posts", response_model=list[PostList])
def list_posts(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> list[Post]:
    """List posts."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    return crud.list_posts(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )



@post.post("/posts", response_model=PostRead, status_code=201)
def create_post(session:Session, data:PostCreate) -> Post:
    """Create a new post."""

    author = get_user_by_id(session, data.author_id)
    post = crud.get_post_by_title(session, data.title)
    if post:
        raise HTTPException(409, f"Post {data.title} already exists!")
    if not author:
        raise HTTPException(404, f"User #{data.author_id} not found!")
    data.author_id = author.profile.id
    return crud.create_post(session, data)



@post.get("/posts/{post_id}", response_model=PostRead)
def get_post(session:Session, post_id:int) -> Post:
    """Get a post by its ID."""

    post = crud.get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(404, f"Post #{post_id} not found!")
    return post



@post.put("/posts/{post_id}", response_model=PostRead)
def update_post(
    session:Session, post_id:int, data:PostUpdate
) -> Post:
    """Update a post."""

    post = crud.update_post(session, post_id, data)
    if not post:
        raise HTTPException(404, f"Post #{post_id} not found!")
    return post



@post.delete("/posts/{post_id}", status_code=204)
def delete_post(
    session:Session, post_id:int, hard:bool=False
) -> None:
    """Delete a post by its ID."""

    post = crud.get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(404, f"Post #{post_id} not found!")
    crud.delete_post(session, post_id, hard)



# Post relationship endpoints

@post.get("/posts/{post_id}/author", response_model=UserRead)
def get_post_author(session:Session, post_id:int):
    """Get the author of a post."""

    post = crud.get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(404, f"Post #{post_id} not found!")
    return post.author.user



@post.get("/posts/{post_id}/tags", response_model=list[TagList])
def list_post_tags(session:Session, post_id:int):
    """Get the tags of a post."""

    post = crud.get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(404, f"Post #{post_id} not found!")
    return post.tags



@post.get("/posts/{post_id}/comments", response_model=list[CommentList])
def list_post_comments(session:Session, post_id:int):
    """Get the comments of a post."""

    post = crud.get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(404, f"Post #{post_id} not found!")
    return post.comments



# Comment endpoints

comment = APIRouter()


@comment.get("/comments", response_model=list[CommentList])
def list_comments(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> list[Comment]:
    """List comments."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    return crud.list_comments(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )



@comment.post("/comments", response_model=CommentRead, status_code=201)
def create_comment(session:Session, data:CommentCreate) -> Comment:
    """Create a new comment."""

    author = get_user_by_id(session, data.author_id)
    post = crud.get_post_by_id(session, data.post_id)
    if not author:
        raise HTTPException(404, f"User #{data.author_id} not found!")
    if not post:
        raise HTTPException(404, f"Post #{data.post_id} not found!")
    if data.parent_id:
        parent = crud.get_comment_by_id(session, data.parent_id)
        if not parent:
            raise HTTPException(404, f"Comment #{data.parent_id} not found!")
    data.author_id = author.profile.id
    return crud.create_comment(session, data)



@comment.get("/comments/{comment_id}", response_model=CommentRead)
def get_comment(session:Session, comment_id:int) -> Comment:
    """Get a comment by its ID."""

    comment = crud.get_comment_by_id(session, comment_id)
    if not comment:
        raise HTTPException(404, f"Comment #{comment_id} not found!")
    return comment



@comment.put("/comments/{comment_id}", response_model=CommentRead)
def update_comment(
    session:Session, comment_id:int, data:CommentUpdate
) -> Comment:
    """Update a comment."""

    comment = crud.update_comment(session, comment_id, data)
    if not comment:
        raise HTTPException(404, f"Comment #{comment_id} not found!")
    return comment



@comment.delete("/comments/{comment_id}", status_code=204)
def delete_comment(
    session:Session, comment_id:int, hard:bool=False
) -> None:
    """Delete a comment by its ID."""

    comment = crud.get_comment_by_id(session, comment_id)
    if not comment:
        raise HTTPException(404, f"Comment #{comment_id} not found!")
    crud.delete_comment(session, comment_id, hard)



# Comment relationship endpoints

@comment.get("/comments/{comment_id}/author", response_model=UserRead)
def get_comment_author(session:Session, comment_id:int):
    """Get the author of a comment."""

    comment = crud.get_comment_by_id(session, comment_id)
    if not comment:
        raise HTTPException(404, f"Comment #{comment_id} not found!")
    return comment.author.user



@comment.get("/comments/{comment_id}/post", response_model=PostRead)
def get_comment_post(session:Session, comment_id:int):
    """Get the post of a comment."""

    comment = crud.get_comment_by_id(session, comment_id)
    if not comment:
        raise HTTPException(404, f"Comment #{comment_id} not found!")
    return comment.post



@comment.get("/comments/{comment_id}/parent", response_model=CommentRead)
def get_comment_parent(session:Session, comment_id:int):
    """Get the parent of a comment."""

    comment = crud.get_comment_by_id(session, comment_id)
    if not comment:
        raise HTTPException(404, f"Comment #{comment_id} not found!")
    return comment.parent



@comment.get(
        "/comments/{comment_id}/reactions",
        response_model=list[CommentReactionList]
)
def list_comment_reactions(session:Session, comment_id:int):
    """Get the reactions of a comment."""

    comment = crud.get_comment_by_id(session, comment_id)
    if not comment:
        raise HTTPException(404, f"Comment #{comment_id} not found!")
    return comment.reactions



@comment.get(
    "/comments/{comment_id}/replies", response_model=list[CommentList]
)
def list_comment_replies(session:Session, comment_id:int):
    """Get the replies of a comment."""

    comment = crud.get_comment_by_id(session, comment_id)
    if not comment:
        raise HTTPException(404, f"Comment #{comment_id} not found!")
    return comment.replies



# CommentReaction endpoints

reaction = APIRouter()


@reaction.get("/reactions", response_model=list[CommentReactionList])
def list_reactions(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> list[CommentReaction]:
    """List reactions."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    return crud.list_reactions(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )



@reaction.post(
    "/reactions", response_model=CommentReactionRead, status_code=201
)
def create_reaction(session:Session, data:CommentReactionCreate) -> CommentReaction:
    """Create a new reaction."""

    author = get_user_by_id(session, data.author_id)
    comment = crud.get_comment_by_id(session, data.comment_id)
    if not author:
        raise HTTPException(404, f"User #{data.author_id} not found!")
    if not comment:
        raise HTTPException(404, f"Comment #{data.comment_id} not found!")
    data.author_id = author.profile.id
    return crud.create_reaction(session, data)



@reaction.get("/reactions/{reaction_id}", response_model=CommentReactionRead)
def get_reaction(session:Session, reaction_id:int) -> CommentReaction:
    """Get a reaction by its ID."""

    reaction = crud.get_reaction_by_id(session, reaction_id)
    if not reaction:
        raise HTTPException(404, f"Comment reaction #{reaction_id} not found!")
    return reaction



@reaction.put("/reactions/{reaction_id}", response_model=CommentReactionRead)
def update_reaction(
    session:Session, reaction_id:int, data:CommentReactionUpdate
) -> CommentReaction:
    """Update a reaction."""

    reaction = crud.update_reaction(session, reaction_id, data)
    if not reaction:
        raise HTTPException(404, f"Comment reaction #{reaction_id} not found!")
    return reaction



@reaction.delete("/reactions/{reaction_id}", status_code=204)
def delete_reaction(
    session:Session, reaction_id:int, hard:bool=False
) -> None:
    """Delete a reaction by its ID."""

    reaction = crud.get_reaction_by_id(session, reaction_id)
    if not reaction:
        raise HTTPException(404, f"Comment reaction #{reaction_id} not found!")
    crud.delete_reaction(session, reaction_id, hard)
