from sqlalchemy import func
from sqlmodel import Session, select

from api.crud.utils import apply_filters, apply_sorting
from api.models.events import Event, Participation, Path, Review
from api.schemas.events import (
    EventCreate, EventUpdate, ParticipationCreate, ParticipationUpdate,
    ReviewCreate, ReviewUpdate, PathCreate, PathUpdate)



# Event model CRUD

def create_event(session:Session, data:EventCreate) -> Event:
    """Create a new event."""

    new_event = Event.model_validate(data)
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return new_event



def get_event_by_id(session:Session, event_id:int) -> Event|None:
    """Get an event by its ID."""

    event = session.get(Event, event_id)
    return event if event and not event.deleted else None



def get_event_by_name(session:Session, name:str) -> Event|None:
    """Get an event by its name."""

    query = select(Event).where(
        func.lower(Event.name) == name.lower(), Event.deleted == False
    )
    return session.exec(query).first()



def list_events(
    session:Session,
    skip:int|None=None,
    limit:int|None=None,
    sort: dict[str, str]|None = None,
    filter: dict[str, any]|None = None
) -> list[Event]:
    """List events."""

    query = select(Event).where(Event.deleted == False)
    if filter:
        query = apply_filters(query, Event, filter)
    if sort:
        query = apply_sorting(query, Event, sort)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return session.exec(query).all()



def count_events(session:Session, filter:dict[str, any]|None=None) -> int:
    query = select(func.count(Event.id)).where(Event.deleted == False)
    if filter:
        query = apply_filters(query, Event, filter)
    return session.exec(query).one()



def update_event(
        session:Session, event_id:int, data:EventUpdate
) -> Event|None:
    """Update an event."""

    event = session.get(Event, event_id)
    if event:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(event, field, value)
        session.commit()
        session.refresh(event)
    return event



def delete_event(session:Session, event_id:int, hard:bool=False) -> None:
    """Delete an event."""

    event = session.get(Event, event_id)
    if event:
        if hard:
            session.delete(event)
            session.commit()
        else:
            event.deleted = True
            session.commit()
            session.refresh(event)



# Participation model CRUD

def create_participation(
        session:Session, profile_id:int, event_id:int, data:ParticipationCreate
) -> Participation:
    """Create a new participation."""

    participation = Participation(
        member_id=profile_id, event_id=event_id, attended=data.attended
    )
    session.add(participation)
    session.commit()
    session.refresh(participation)
    return participation



def get_participation(
        session:Session, profile_id:int, event_id:int
) -> Participation|None:
    """Get a participation."""

    query = select(Participation).where(
        Participation.member_id == profile_id,
        Participation.event_id == event_id
    )
    return session.exec(query).first()



def update_participation(
        session:Session, participation:Participation, data:ParticipationUpdate
) -> Participation:
    """Update a participation."""

    participation.attended = data.attended
    session.add(participation)
    session.commit()
    session.refresh(participation)
    return participation



def delete_participation(
        session:Session, participation:Participation, hard:bool|None=None
) -> None:
    """Delete a participation."""

    if hard:
        session.delete(participation)
        session.commit()
    else:
        participation.deleted = True
        session.commit()
        session.refresh(participation)



# Review model CRUD

def create_review(
        session:Session, profile_id:int, event_id:int, data:ReviewCreate
) -> Review:
    """Create a new review."""

    review = Review(
        author_id=profile_id,
        event_id=event_id,
        attended=data.comment,
        score=data.score
    )
    session.add(review)
    session.commit()
    session.refresh(review)
    return review



def get_review(
        session:Session, profile_id:int, event_id:int
) -> Review|None:
    """Get a review."""

    query = select(Review).where(
        Review.author_id == profile_id,
        Review.event_id == event_id
    )
    return session.exec(query).first()



def update_review(
        session:Session, review:Review, data:ReviewUpdate
) -> Review:
    """Update a review."""

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(review, field, value)
    session.commit()
    session.refresh(review)
    return review



def delete_review(
        session:Session, review:Review, hard:bool|None=None
) -> None:
    """Delete a review."""

    if hard:
        session.delete(review)
        session.commit()
    else:
        review.deleted = True
        session.commit()
        session.refresh(review)



# Path model CRUD

def create_path(session:Session, data:PathCreate) -> Path:
    """Create an path."""

    new_path = Path.model_validate(data)
    session.add(new_path)
    session.commit()
    session.refresh(new_path)
    return new_path



def get_path_by_id(session:Session, path_id:int) -> Path|None:
    """Get an path by its ID."""

    path = session.get(Path, path_id)
    return path if path and not path.deleted else None



def get_path_by_name(session:Session, name:str) -> Path|None:
    """Get an path by its name."""

    query = select(Path).where(
        func.lower(Path.name) == name.lower(), Path.deleted == False
    )
    return session.exec(query).first()



def list_paths(
    session:Session,
    skip:int|None=None,
    limit:int|None=None,
    sort: dict[str, str]|None = None,
    filter: dict[str, any]|None = None
) -> list[Path]:
    """List paths."""

    query = select(Path).where(Path.deleted == False)
    if filter:
        query = apply_filters(query, Path, filter)
    if sort:
        query = apply_sorting(query, Path, sort)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return session.exec(query).all()



def count_paths(session:Session, filter:dict[str, any]|None=None) -> int:
    query = select(func.count(Path.id)).where(Path.deleted == False)
    if filter:
        query = apply_filters(query, Path, filter)
    return session.exec(query).one()



def update_path(
        session:Session, path_id:int, data:PathUpdate
) -> Path|None:
    """Update an path."""

    path = session.get(Path, path_id)
    if path:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(path, field, value)
        session.commit()
        session.refresh(path)
    return path



def delete_path(
        session:Session, path_id:int, hard:bool=False
) -> None:
    """Delete an path."""

    path = session.get(Path, path_id)
    if path:
        if hard:
            session.delete(path)
            session.commit()
        else:
            path.deleted = True
            session.commit()
            session.refresh(path)
