from sqlmodel import Session, select

from api.models.feedbacks import Feedback, FeedbackAnswer
from api.models.utils.enums import FeedbackStatus, FeedbackType
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
    feedback_type:FeedbackType|None=None,
    status:FeedbackStatus|None=None,
    member_id:int|None=None
) -> list[Feedback]:
    """List feedbacks."""

    query = select(Feedback).where(Feedback.deleted == False)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    if feedback_type is not None:
        query = query.where(Feedback.type == feedback_type)
    if status is not None:
        query = query.where(Feedback.status == status)
    if member_id is not None:
        query = query.where(Feedback.member_id == member_id)
    return session.exec(query).all()



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
    member_id:int|None=None,
    feedback_id:int|None=None
) -> list[FeedbackAnswer]:
    """List feedback_answers."""

    query = select(FeedbackAnswer).where(FeedbackAnswer.deleted == False)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    if member_id is not None:
        query = query.where(FeedbackAnswer.member_id == member_id)
    if feedback_id is not None:
        query = query.where(FeedbackAnswer.feedback_id == feedback_id)
    return session.exec(query).all()



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
