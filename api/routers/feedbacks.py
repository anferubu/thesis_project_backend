from fastapi import APIRouter, HTTPException

from api.crud import feedbacks as crud
from api.crud.users import get_user_by_id
from api.crud.utils import parse_filter_param, parse_sort_param
from api.models.feedbacks import Feedback, FeedbackAnswer
from api.schemas.feedbacks import (
    FeedbackCreate, FeedbackUpdate, FeedbackRead, FeedbackList,
    FeedbackAnswerCreate, FeedbackAnswerUpdate, FeedbackAnswerRead,
    FeedbackAnswerList)
from api.schemas.users import UserRead
from core.database import DBSession as Session



feedback = APIRouter()



# Feedback endpoints

@feedback.get("/feedbacks", response_model=dict)
def list_feedbacks(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> dict:
    """List feedbacks."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    total_records = crud.count_feedbacks(session, filter_dict)
    current_page = (skip // limit) + 1 if limit else 1
    total_pages = (total_records + limit - 1) // limit if limit else 1
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    feedbacks = crud.list_feedbacks(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )

    return {
        "data": feedbacks,
        "pagination": {
            "total_records": total_records,
            "per_page": limit,
            "current_page": current_page,
            "total_pages": total_pages,
            "next_page": next_page,
            "prev_page": prev_page
        }
    }



@feedback.post("/feedbacks", response_model=FeedbackRead, status_code=201)
def create_feedback(session:Session, data:FeedbackCreate) -> Feedback:
    """Create a new feedback."""

    author = get_user_by_id(session, data.author_id)
    if not author:
        raise HTTPException(404, f"User #{data.author_id} not found!")
    data.author_id = author.profile.id
    return crud.create_feedback(session, data)



@feedback.get("/feedbacks/{feedback_id}", response_model=FeedbackRead)
def get_feedback(session:Session, feedback_id:int) -> Feedback:
    """Get a feedback by its ID."""

    feedback = crud.get_feedback_by_id(session, feedback_id)
    if not feedback:
        raise HTTPException(404, f"Feedback #{feedback_id} not found!")
    return feedback



@feedback.put("/feedbacks/{feedback_id}", response_model=FeedbackRead)
def update_feedback(
    session:Session, feedback_id:int, data:FeedbackUpdate
) -> Feedback:
    """Update a feedback."""

    feedback = crud.update_feedback(session, feedback_id, data)
    if not feedback:
        raise HTTPException(404, f"Feedback #{feedback_id} not found!")
    return feedback



@feedback.delete("/feedbacks/{feedback_id}", status_code=204)
def delete_feedback(
    session:Session, feedback_id:int, hard:bool=False
) -> None:
    """Delete a feedback by its ID."""

    feedback = crud.get_feedback_by_id(session, feedback_id)
    if not feedback:
        raise HTTPException(404, f"Feedback #{feedback_id} not found!")
    crud.delete_feedback(session, feedback_id, hard)



# Feedback relationship endpoints

@feedback.get("/feedbacks/{feedback_id}/author", response_model=UserRead)
def get_feedback_author(session:Session, feedback_id:int):
    """Get the author of a feedback."""

    feedback = crud.get_feedback_by_id(session, feedback_id)
    if not feedback:
        raise HTTPException(404, f"Feedback #{feedback_id} not found!")
    return feedback.author.user



@feedback.get("/feedbacks/{feedback_id}/answer", response_model=FeedbackAnswerRead)
def get_feedback_answer(session:Session, feedback_id:int):
    """Get the answer of a feedback."""

    feedback = crud.get_feedback_by_id(session, feedback_id)
    if not feedback:
        raise HTTPException(404, f"Feedback #{feedback_id} not found!")
    return feedback.answer



# FeedbackAnswer endpoints

answer = APIRouter()


@answer.get("/feedback_answers", response_model=dict)
def list_feedback_answers(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> dict:
    """List feedback answers."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    total_records = crud.count_feedback_answers(session, filter_dict)
    current_page = (skip // limit) + 1 if limit else 1
    total_pages = (total_records + limit - 1) // limit if limit else 1
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    feedback_answers = crud.list_feedback_answers(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )

    return {
        "data": feedback_answers,
        "pagination": {
            "total_records": total_records,
            "per_page": limit,
            "current_page": current_page,
            "total_pages": total_pages,
            "next_page": next_page,
            "prev_page": prev_page
        }
    }



@answer.post(
    "/feedback_answers", response_model=FeedbackAnswerRead, status_code=201
)
def create_feedback_answer(
    session:Session, data:FeedbackAnswerCreate
) -> FeedbackAnswer:
    """Create a new feedback answer."""

    author = get_user_by_id(session, data.author_id)
    answer = crud.list_feedback_answers(session, filter={"feedback_id": data.feedback_id, "author_id": data.author_id})
    if answer:
        raise HTTPException(409, f"La consulta ya ha sido resuelta por el usuario #{answer.author_id}")
    if not author:
        raise HTTPException(404, f"User #{data.author_id} not found!")
    data.author_id = author.profile.id
    return crud.create_feedback_answer(session, data)



@answer.get(
    "/feedback_answers/{feedback_answer_id}",
    response_model=FeedbackAnswerRead
)
def get_feedback_answer(
    session:Session, feedback_answer_id:int
) -> FeedbackAnswer:
    """Get a feedback answer by its ID."""

    feedback_answer = crud.get_feedback_answer_by_id(session, feedback_answer_id)
    if not feedback_answer:
        raise HTTPException(404, f"Feedback answer #{feedback_answer_id} not found!")
    return feedback_answer



@answer.put(
        "/feedback_answers/{feedback_answer_id}",
        response_model=FeedbackAnswerRead
)
def update_feedback_answer(
    session:Session, feedback_answer_id:int, data:FeedbackAnswerUpdate
) -> FeedbackAnswer:
    """Update a feedback answer."""

    feedback_answer = crud.update_feedback_answer(session, feedback_answer_id, data)
    if not feedback_answer:
        raise HTTPException(404, f"Feedback answer #{feedback_answer_id} not found!")
    return feedback_answer



@answer.delete("/feedback_answers/{feedback_answer_id}", status_code=204)
def delete_feedback_answer(
    session:Session, feedback_answer_id:int, hard:bool=False
) -> None:
    """Delete a feedback answer by its ID."""

    feedback_answer = crud.get_feedback_answer_by_id(session, feedback_answer_id)
    if not feedback_answer:
        raise HTTPException(404, f"Feedback answer #{feedback_answer_id} not found!")
    crud.delete_feedback_answer(session, feedback_answer_id, hard)



# FeedbackAnswer relationship endpoints

@answer.get(
        "/feedback_answers/{feedback_answer_id}/author",
        response_model=UserRead
)
def get_feedback_answer_author(session:Session, feedback_answer_id:int):
    """Get the author of a feedback answer."""

    feedback_answer = crud.get_feedback_answer_by_id(session, feedback_answer_id)
    if not feedback_answer:
        raise HTTPException(404, f"Feedback answer #{feedback_answer_id} not found!")
    return feedback_answer.author.user



@answer.get(
        "/feedback_answers/{feedback_answer_id}/feedback",
        response_model=FeedbackRead
)
def get_feedback_answer_feedback(session:Session, feedback_answer_id:int):
    """Get the feedback of an answer."""

    feedback_answer = crud.get_feedback_answer_by_id(session, feedback_answer_id)
    if not feedback_answer:
        raise HTTPException(404, f"Feedback answer #{feedback_answer_id} not found!")
    return feedback_answer.feedback
