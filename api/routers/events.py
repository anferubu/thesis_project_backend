from fastapi import APIRouter, HTTPException

from api.crud import events as crud
from api.crud.events import get_event_by_id
from api.crud.users import get_member_by_id, get_user_by_id
from api.crud.utils import parse_filter_param, parse_sort_param
from api.models.events import Event, Participation, Review, Path
from api.schemas.events import (
    EventCreate, EventRead, EventUpdate, EventList,
    ParticipationCreate, ParticipationRead, ParticipationUpdate,
    ParticipationEventList, ParticipationMemberList,
    ReviewCreate, ReviewRead, ReviewUpdate, ReviewEventList, ReviewMemberList,
    PathCreate, PathRead, PathUpdate, PathList
)
from api.schemas.teams import LocationRead, TeamRead
from api.schemas.users import MemberRead
from core.database import DBSession as Session



event = APIRouter()



# Event endpoints

@event.get("/events", response_model=list[EventList])
def list_events(
    session:Session,
    skip:int=0,
    limit:int=10,
    sort:str|None=None,
    filter:str|None=None
) -> list[Event]:
    """List events."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    return crud.list_events(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )



@event.post("/events", response_model=EventRead, status_code=201)
def create_event(session:Session, data:EventCreate) -> Event:
    """Create a new event."""

    event = crud.get_event_by_name(session, data.name)
    if event:
        raise HTTPException(409, f"Event {data.name} already exists!")
    return crud.create_event(session, data)



@event.get("/events/{event_id}", response_model=EventRead)
def get_event(session:Session, event_id:int) -> Event:
    """Get an event by its ID."""

    event = crud.get_event_by_id(session, event_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    return event



@event.put("/events/{event_id}", response_model=EventRead)
def update_event(session:Session, event_id:int, data:EventUpdate) -> Event:
    """Update an event."""

    event = crud.update_event(session, event_id, data)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    return event



@event.delete("/events/{event_id}", status_code=204)
def delete_event(session:Session, event_id:int, hard:bool=False) -> None:
    """Delete an event by its ID."""

    event = crud.get_event_by_id(session, event_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    crud.delete_event(session, event_id, hard)



# Event relationship endpoints

@event.get("/events/{event_id}/location", response_model=LocationRead)
def get_event_location(session:Session, event_id:int):
    """Get the location of an event."""

    event = crud.get_event_by_id(session, event_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    return event.location



@event.get("/events/{event_id}/organizer", response_model=MemberRead)
def get_event_organizer(session:Session, event_id:int):
    """Get the organizer of an event."""

    event = crud.get_event_by_id(session, event_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    return event.organizer



@event.get("/events/{event_id}/team", response_model=TeamRead)
def get_event_team(session:Session, event_id:int):
    """Get the team of an event."""

    event = crud.get_event_by_id(session, event_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    return event.team



@event.get("/events/{event_id}/path", response_model=PathRead)
def get_event_path(session:Session, event_id:int):
    """Get the path of an event."""

    event = crud.get_event_by_id(session, event_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    if event.path is None:
        raise HTTPException(404, f"No path found for event #{event_id}!")
    return event.path



# Participation endpoints

participation = APIRouter()


@participation.post(
    "/events/{event_id}/users/{user_id}/participations",
    response_model=list[ParticipationRead]
)
def create_participation(
    session:Session, event_id:int, user_id:int, data:ParticipationCreate
) -> list[Participation]:
    """Create a new participation for a member in an event."""

    event = get_event_by_id(session, event_id)
    user = get_user_by_id(session, user_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    if not user:
        raise HTTPException(404, f"User #{user_id} not found!")
    participation = crud.get_participation(session, user.profile.id, event_id)
    if not participation:
        new_participation = crud.create_participation(
            session, user.profile.id, event_id, data
        )
        event.members.append(new_participation)
        return event.members
    else:
        raise HTTPException(
            400,
            f"User #{user_id} is already part of the event #{event_id}!"
        )



@participation.get(
    "/events/{event_id}/participations",
    response_model=list[ParticipationMemberList]
)
def list_event_participations(
    session:Session, event_id:int, attended:bool|None=None
) -> list[Participation]:
    """List participations for an event."""

    event = get_event_by_id(session, event_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    if attended is not None:
        participations = [
            participation for participation in event.members
            if participation.attended == attended
        ]
    else:
        participations = event.members
    return participations



@participation.get(
        "/members/{member_id}/participations",
        response_model=list[ParticipationEventList]
)
def list_member_participations(
    session:Session, member_id:int, attended:bool|None=None
) -> list[Participation]:
    """List participations for a member."""

    member = get_member_by_id(session, member_id)
    if not member:
        raise HTTPException(404, f"Member #{member_id} not found!")
    if attended is not None:
        participations = [
            participation for participation in member.attended_events
            if participation.attended == attended
        ]
    else:
        participations = member.attended_events
    return participations



@participation.get(
    "/events/{event_id}/members/{member_id}/participations",
    response_model=ParticipationRead
)
def get_participation(
    session:Session, event_id:int, member_id:int
) -> Participation:
    """Get a participation for a member in an event."""

    participation = crud.get_participation(session, event_id, member_id)
    if not participation:
        raise HTTPException(
            404, f"Member #{member_id} not participate in event #{event_id}!"
        )
    return participation



@participation.put(
    "/events/{event_id}/members/{member_id}/participations",
    response_model=Participation
)
def update_participation(
    session:Session,
    event_id:int,
    member_id:int,
    data:ParticipationUpdate
) -> Participation:
    """Update a participation for a member in an event."""

    participation = crud.get_participation(session, member_id, event_id)
    if not participation:
        raise HTTPException(
            404, f"Member #{member_id} not participate in event #{event_id}!"
        )
    participation = crud.update_participation(session, participation, data)
    return participation



@participation.delete(
    "/events/{event_id}/members/{member_id}/participations", status_code=204
)
def remove_member_from_event(
    session:Session, event_id:int, member_id:int, hard:bool=False
) -> None:
    """Remove a member from an event."""

    event = get_event_by_id(session, event_id)
    member = get_member_by_id(session, member_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    if not member:
        raise HTTPException(404, f"Member #{member_id} not found!")
    participation = crud.get_participation(session, event_id, member_id)
    if participation:
        crud.delete_participation(session, participation, hard)
    else:
        raise HTTPException(
            404, f"Member #{member_id} not found in event #{event_id}!"
        )



# Review endpoints

review = APIRouter()


@review.post(
    "/events/{event_id}/members/{member_id}/reviews",
    response_model=list[ReviewRead]
)
def create_review(
    session:Session, event_id:int, member_id:int, data:ReviewCreate
) -> list[Review]:
    """Create a new user review for an event."""

    event = get_event_by_id(session, event_id)
    member = get_member_by_id(session, member_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    if not member:
        raise HTTPException(404, f"Member #{member_id} not found!")
    participation = get_participation(session, member_id, event_id)
    if not participation:
        raise HTTPException(
            404,
            f"Member #{member_id} didn't confirm attendance at event #{event_id}!"
        )
    if not participation.attended:
        raise HTTPException(
            404, f"Member #{member_id} didn't attend the event #{event_id}!"
        )
    review = crud.get_review(session, member_id, event_id)
    if not review:
        new_review = crud.create_review(session, member_id, event_id, data)
        event.reviews.append(new_review)
        return event.reviews
    else:
        raise HTTPException(
            400,
            f"Member #{member_id} has already made a review of the event #{event_id}!"
        )



@review.get(
    "/events/{event_id}/reviews",
    response_model=list[ReviewMemberList]
)
def list_event_reviews(
    session:Session, event_id:int, score:int|None=None
) -> list[Review]:
    """List reviews made for an event."""

    event = get_event_by_id(session, event_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    if score is not None:
        reviews = [
            review for review in event.reviews
            if review.score == score
        ]
    else:
        reviews = event.reviews
    return reviews



@review.get(
        "/members/{member_id}/reviews",
        response_model=list[ReviewEventList]
)
def list_member_reviews(
    session:Session, member_id:int, score:int|None=None
) -> list[Review]:
    """List reviews made by a member."""

    member = get_member_by_id(session, member_id)
    if not member:
        raise HTTPException(404, f"Member #{member_id} not found!")
    if score is not None:
        reviews = [
            review for review in member.reviews
            if review.score == score
        ]
    else:
        reviews = member.reviews
    return reviews



@review.get(
    "/events/{event_id}/members/{member_id}/reviews",
    response_model=ReviewRead
)
def get_review(
    session:Session, event_id:int, member_id:int
) -> Review:
    """get a user review for an event."""

    review = crud.get_review(session, event_id, member_id)
    if not review:
        raise HTTPException(
            404,
            f"Member #{member_id} has not made any reviews of the event #{event_id}!"
        )
    return review



@review.put(
    "/events/{event_id}/members/{member_id}/reviews",
    response_model=Review
)
def update_review(
    session:Session,
    event_id:int,
    member_id:int,
    data:ReviewUpdate
) -> Review:
    """Update a user review for an event."""

    review = crud.get_review(session, member_id, event_id)
    if not review:
        raise HTTPException(
            404,
            f"Member #{member_id} has not made any reviews of the event #{event_id}!"
        )
    review = crud.update_review(session, review, data)
    return review



@review.delete(
    "/events/{event_id}/members/{member_id}/reviews",
    status_code=204
)
def delete_review(
    session:Session, event_id:int, member_id:int, hard:bool=False
) -> None:
    """Delete a user review for a particular event."""

    event = get_event_by_id(session, event_id)
    member = get_member_by_id(session, member_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    if not member:
        raise HTTPException(404, f"Member #{member_id} not found!")
    review = crud.get_review(session, event_id, member_id)
    if review:
        crud.delete_review(session, review, hard)
    else:
        raise HTTPException(
            404,
            f"Member #{member_id} has not made any reviews of the event #{event_id}!"
        )



# Path endpoints

path = APIRouter()


@path.get("/paths", response_model=list[PathList])
def list_paths(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> list[Path]:
    """List paths."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    return crud.list_paths(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )



@path.post("/paths", response_model=PathRead, status_code=201)
def create_path(session:Session, data:PathCreate) -> Path:
    """Create a new path."""

    path = crud.get_path_by_name(session, data.name)
    if path:
        raise HTTPException(409, f"Path {data.name} already exists!")
    return crud.create_path(session, data)



@path.get("/paths/{path_id}", response_model=PathRead)
def get_path(session:Session, path_id:int) -> Path:
    """Get a path by its ID."""

    path = crud.get_path_by_id(session, path_id)
    if not path:
        raise HTTPException(404, f"Path #{path_id} not found!")
    return path



@path.put("/paths/{path_id}", response_model=PathRead)
def update_path(
    session:Session, path_id:int, data:PathUpdate
) -> Path:
    """Update a path."""

    path = crud.update_path(session, path_id, data)
    if not path:
        raise HTTPException(404, f"Path #{path_id} not found!")
    return path



@path.delete("/paths/{path_id}", status_code=204)
def delete_path(
    session:Session, path_id:int, hard:bool=False
) -> None:
    """Delete a path by its ID."""

    path = crud.get_path_by_id(session, path_id)
    if not path:
        raise HTTPException(404, f"Path #{path_id} not found!")
    crud.delete_path(session, path_id, hard)



# Path relationship endpoints

@path.get("/paths/{path_id}/events", response_model=list[EventList])
def list_path_events(session:Session, path_id:int):
    """Get the events related with a path."""

    path = crud.get_path_by_id(session, path_id)
    if not path:
        raise HTTPException(404, f"Path #{path_id} not found!")
    return path.events
