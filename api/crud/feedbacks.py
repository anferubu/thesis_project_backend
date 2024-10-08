from sqlalchemy import func
from sqlmodel import Session, select

from api.crud.utils import apply_filters, apply_sorting
from api.models.feedbacks import Feedback, FeedbackAnswer
from api.schemas.feedbacks import (
   FeedbackCreate, FeedbackUpdate, FeedbackAnswerCreate, FeedbackAnswerUpdate)



#Feedback model CRUD

def create_feedback(session:Session, data:FeedbackCreate) -> Feedback:
    """Create a feedback."""

    new_feedback = Feedback.model_validate(data)
    session.add(new_feedback)
    session.commit()
    session.refresh(new_feedback)
    return new_feedback



def get_feedback_by_id(session:Session, feedback_id:int) -> Feedback|None:
    """Get a feedback by its ID."""

    feedback = session.get(Feedback, feedback_id)
    return feedback if feedback and not feedback.deleted else None



def list_feedbacks(
    session:Session,
    skip:int|None=None,
    limit:int|None=None,
    sort: dict[str, str]|None = None,
    filter: dict[str, any]|None = None
) -> list[Feedback]:
    """List feedbacks."""

    query = select(Feedback).where(Feedback.deleted == False)
    if filter:
        query = apply_filters(query, Feedback, filter)
    if sort:
        query = apply_sorting(query, Feedback, sort)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return session.exec(query).all()



def count_feedbacks(session:Session, filter:dict[str, any]|None=None) -> int:
    query = select(func.count(Feedback.id)).where(Feedback.deleted == False)
    if filter:
        query = apply_filters(query, Feedback, filter)
    return session.exec(query).one()



def update_feedback(
        session:Session, feedback_id:int, data:FeedbackUpdate
) -> Feedback|None:
    """Update a feedback."""

    feedback = session.get(Feedback, feedback_id)
    if feedback:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(feedback, field, value)
        session.commit()
        session.refresh(feedback)
    return feedback



def delete_feedback(
        session:Session, feedback_id:int, hard:bool=False
) -> None:
    """Delete a feedback."""

    feedback = session.get(Feedback, feedback_id)
    if feedback:
        if hard:
            session.delete(feedback)
            session.commit()
        else:
            feedback.deleted = True
            session.commit()
            session.refresh(feedback)



# FeedbackAnswer model CRUD

def create_feedback_answer(
        session:Session, data:FeedbackAnswerCreate
) -> FeedbackAnswer:
    """Create a feedback_answer."""

    new_feedback_answer = FeedbackAnswer.model_validate(data)
    session.add(new_feedback_answer)
    session.commit()
    session.refresh(new_feedback_answer)
    return new_feedback_answer



def get_feedback_answer_by_id(
        session:Session, feedback_answer_id:int
) -> FeedbackAnswer|None:
    """Get a feedback_answer by its ID."""

    feedback_answer = session.get(FeedbackAnswer, feedback_answer_id)
    return feedback_answer if feedback_answer and not feedback_answer.deleted else None



def list_feedback_answers(
    session:Session,
    skip:int|None=None,
    limit:int|None=None,
    sort: dict[str, str]|None = None,
    filter: dict[str, any]|None = None
) -> list[FeedbackAnswer]:
    """List feedback_answers."""

    query = select(FeedbackAnswer).where(FeedbackAnswer.deleted == False)
    if filter:
        query = apply_filters(query, FeedbackAnswer, filter)
    if sort:
        query = apply_sorting(query, FeedbackAnswer, sort)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return session.exec(query).all()



def count_feedback_answers(session:Session, filter:dict[str, any]|None=None) -> int:
    query = select(func.count(FeedbackAnswer.id)).where(FeedbackAnswer.deleted == False)
    if filter:
        query = apply_filters(query, FeedbackAnswer, filter)
    return session.exec(query).one()



def update_feedback_answer(
        session:Session, feedback_answer_id:int, data:FeedbackAnswerUpdate
) -> FeedbackAnswer|None:
    """Update a feedback_answer."""

    feedback_answer = session.get(FeedbackAnswer, feedback_answer_id)
    if feedback_answer:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(feedback_answer, field, value)
        session.commit()
        session.refresh(feedback_answer)
    return feedback_answer



def delete_feedback_answer(
        session:Session, feedback_answer_id:int, hard:bool=False
) -> None:
    """Delete a feedback_answer."""

    feedback_answer = session.get(FeedbackAnswer, feedback_answer_id)
    if feedback_answer:
        if hard:
            session.delete(feedback_answer)
            session.commit()
        else:
            feedback_answer.deleted = True
            session.commit()
            session.refresh(feedback_answer)
