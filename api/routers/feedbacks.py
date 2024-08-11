from fastapi import APIRouter, HTTPException

from api.crud import feedbacks as crud
from api.models.feedbacks import Feedback, FeedbackAnswer
from api.models.utils.enums import FeedbackStatus, FeedbackType
from api.schemas.feedbacks import (
    FeedbackCreate, FeedbackUpdate, FeedbackRead, FeedbackList,
    FeedbackAnswerCreate, FeedbackAnswerUpdate, FeedbackAnswerRead,
    FeedbackAnswerList)
from api.schemas.users import MemberRead
from core.database import DBSession as Session



router = APIRouter()



# Feedback endpoints

@router.get("/feedbacks", response_model=list[FeedbackList])
def list_feedbacks(
    session:Session,
    skip:int=0,
    limit:int=10,
    feedback_type:FeedbackType|None=None,
    status:FeedbackStatus|None=None,
    member_id:int|None=None
) -> list[Feedback]:
    """List feedbacks."""

    return crud.list_feedbacks(
        session, skip, limit, feedback_type, status, member_id
    )



@router.post("/feedbacks", response_model=FeedbackRead, status_code=201)
def create_feedback(session:Session, data:FeedbackCreate) -> Feedback:
    """Create a new feedback."""

    return crud.create_feedback(session, data)



@router.get("/feedbacks/{feedback_id}", response_model=FeedbackRead)
def get_feedback(session:Session, feedback_id:int) -> Feedback:
    """Get a feedback by its ID."""

    feedback = crud.get_feedback_by_id(session, feedback_id)
    if not feedback:
        raise HTTPException(404, f"Feedback #{feedback_id} not found!")
    return feedback



@router.put("/feedbacks/{feedback_id}", response_model=FeedbackRead)
def update_feedback(
    session:Session, feedback_id:int, data:FeedbackUpdate
) -> Feedback:
    """Update a feedback."""

    feedback = crud.update_feedback(session, feedback_id, data)
    if not feedback:
        raise HTTPException(404, f"Feedback #{feedback_id} not found!")
    return feedback



@router.delete("/feedbacks/{feedback_id}", status_code=204)
def delete_feedback(
    session:Session, feedback_id:int, hard:bool=False
) -> None:
    """Delete a feedback by its ID."""

    feedback = crud.get_feedback_by_id(session, feedback_id)
    if not feedback:
        raise HTTPException(404, f"Feedback #{feedback_id} not found!")
    crud.delete_feedback(session, feedback_id, hard)



# Feedback relationship endpoints

@router.get("/feedbacks/{feedback_id}/author", response_model=MemberRead)
def list_feedback_author(session:Session, feedback_id:int):
    """Get the author of a feedback."""

    feedback = crud.get_feedback_by_id(session, feedback_id)
    if not feedback:
        raise HTTPException(404, f"Feedback #{feedback_id} not found!")
    return feedback.member



@router.get("/feedbacks/{feedback_id}/answer", response_model=FeedbackAnswerRead)
def list_feedback_answer(session:Session, feedback_id:int):
    """Get the answer of a feedback."""

    feedback = crud.get_feedback_by_id(session, feedback_id)
    if not feedback:
        raise HTTPException(404, f"Feedback #{feedback_id} not found!")
    return feedback.answer



# FeedbackAnswer endpoints

@router.get("/feedback_answers", response_model=list[FeedbackAnswerList])
def list_feedback_answers(
    session:Session,
    skip:int=0,
    limit:int=10,
    member_id:int|None=None,
    feedback_id:int|None=None
) -> list[FeedbackAnswer]:
    """List feedback answers."""

    return crud.list_feedback_answers(
        session, skip, limit, member_id, feedback_id
    )



@router.post(
    "/feedback_answers", response_model=FeedbackAnswerRead, status_code=201
)
def create_feedback_answer(
    session:Session, data:FeedbackAnswerCreate
) -> FeedbackAnswer:
    """Create a new feedback answer."""

    return crud.create_feedback_answer(session, data)



@router.get(
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



@router.put(
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



@router.delete("/feedback_answers/{feedback_answer_id}", status_code=204)
def delete_feedback_answer(
    session:Session, feedback_answer_id:int, hard:bool=False
) -> None:
    """Delete a feedback answer by its ID."""

    feedback_answer = crud.get_feedback_answer_by_id(session, feedback_answer_id)
    if not feedback_answer:
        raise HTTPException(404, f"Feedback answer #{feedback_answer_id} not found!")
    crud.delete_feedback_answer(session, feedback_answer_id, hard)



# FeedbackAnswer relationship endpoints

@router.get(
        "/feedback_answers/{feedback_answer_id}/author",
        response_model=MemberRead
)
def list_feedback_answer_author(session:Session, feedback_answer_id:int):
    """Get the author of a feedback answer."""

    feedback_answer = crud.get_feedback_answer_by_id(session, feedback_answer_id)
    if not feedback_answer:
        raise HTTPException(404, f"Feedback answer #{feedback_answer_id} not found!")
    return feedback_answer.member



@router.get(
        "/feedback_answers/{feedback_answer_id}/feedback",
        response_model=FeedbackRead
)
def list_feedback_answer_feedback(session:Session, feedback_answer_id:int):
    """Get the author of a feedback answer."""

    feedback_answer = crud.get_feedback_answer_by_id(session, feedback_answer_id)
    if not feedback_answer:
        raise HTTPException(404, f"Feedback answer #{feedback_answer_id} not found!")
    return feedback_answer.feedback
