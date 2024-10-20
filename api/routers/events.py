from fastapi import APIRouter, HTTPException

from api.crud import events as crud
from api.crud.events import get_event_by_id
from api.crud.teams import get_location_by_id, get_team_by_id
from api.crud.users import get_user_by_id
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
from api.schemas.users import UserRead
from core.database import DBSession as Session



event = APIRouter()



# Event endpoints

@event.get("/events", response_model=dict)
def list_events(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> dict:
    """List events."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    total_records = crud.count_events(session, filter_dict)
    current_page = (skip // limit) + 1 if limit else 1
    total_pages = (total_records + limit - 1) // limit if limit else 1
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    events = crud.list_events(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )

    return {
        "data": events,
        "pagination": {
            "total_records": total_records,
            "per_page": limit,
            "current_page": current_page,
            "total_pages": total_pages,
            "next_page": next_page,
            "prev_page": prev_page
        }
    }



@event.post("/events", response_model=EventRead, status_code=201)
def create_event(session:Session, data:EventCreate) -> Event:
    """Create a new event."""

    event = crud.get_event_by_name(session, data.name)
    location = get_location_by_id(session, data.location_id)
    organizer = get_user_by_id(session, data.organizer_id)
    team = get_team_by_id(session, data.team_id)
    if event:
        raise HTTPException(409, f"Event {data.name} already exists!")
    if not location:
        raise HTTPException(404, f"Location #{data.location_id} not found!")
    if not organizer:
        raise HTTPException(404, f"User #{data.organizer_id} not found!")
    if not team:
        raise HTTPException(404, f"Team #{data.team_id} not found!")
    if data.path_id:
        path = crud.get_path_by_id(session, data.path_id)
        if not path:
            raise HTTPException(404, f"Path #{data.path_id} not found!")
    data.organizer_id = organizer.profile.id
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



@event.get("/events/{event_id}/organizer", response_model=UserRead)
def get_event_organizer(session:Session, event_id:int):
    """Get the organizer of an event."""

    event = crud.get_event_by_id(session, event_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    return event.organizer.user



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
    """Create a new participation for a user in an event."""

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
        "/users/{user_id}/participations",
        response_model=list[ParticipationEventList]
)
def list_user_participations(
    session:Session, user_id:int, attended:bool|None=None
) -> list[Participation]:
    """List participations for a user."""

    user = get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(404, f"User #{user_id} not found!")
    if attended is not None:
        participations = [
            participation for participation in user.profile.attended_events
            if participation.attended == attended
        ]
    else:
        participations = user.profile.attended_events
    return participations



@participation.get(
    "/events/{event_id}/users/{user_id}/participations",
    response_model=ParticipationRead
)
def get_participation(
    session:Session, event_id:int, user_id:int
) -> Participation:
    """Get a participation for a user in an event."""

    user = get_user_by_id(session, user_id)
    participation = crud.get_participation(session, user.profile.id, event_id)
    if not participation:
        raise HTTPException(
            404, f"User #{user_id} not participate in event #{event_id}!"
        )
    return participation



@participation.put(
    "/events/{event_id}/users/{user_id}/participations",
    response_model=Participation
)
def update_participation(
    session:Session,
    event_id:int,
    user_id:int,
    data:ParticipationUpdate
) -> Participation:
    """Update a participation for a user in an event."""

    user = get_user_by_id(session, user_id)
    participation = crud.get_participation(session, user.profile.id, event_id)
    if not participation:
        raise HTTPException(
            404, f"User #{user_id} not participate in event #{event_id}!"
        )
    participation = crud.update_participation(session, participation, data)
    return participation



@participation.delete(
    "/events/{event_id}/users/{user_id}/participations", status_code=204
)
def remove_user_from_event(
    session:Session, event_id:int, user_id:int, hard:bool=False
) -> None:
    """Remove a user from an event."""

    event = get_event_by_id(session, event_id)
    user = get_user_by_id(session, user_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    if not user:
        raise HTTPException(404, f"User #{user_id} not found!")
    participation = crud.get_participation(session, user.profile.id, event_id)
    if participation:
        crud.delete_participation(session, participation, hard)
    else:
        raise HTTPException(
            404, f"User #{user_id} not found in event #{event_id}!"
        )



# Review endpoints

review = APIRouter()


@review.post(
    "/events/{event_id}/users/{user_id}/reviews",
    response_model=list[ReviewRead]
)
def create_review(
    session:Session, event_id:int, user_id:int, data:ReviewCreate
) -> list[Review]:
    """Create a new user review for an event."""

    event = get_event_by_id(session, event_id)
    user = get_user_by_id(session, user_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    if not user:
        raise HTTPException(404, f"User #{user_id} not found!")
    participation = get_participation(session, user.profile.id, event_id)
    if not participation:
        raise HTTPException(
            404,
            f"User #{user_id} didn't confirm attendance at event #{event_id}!"
        )
    if not participation.attended:
        raise HTTPException(
            404, f"User #{user_id} didn't attend the event #{event_id}!"
        )
    review = crud.get_review(session, user.profile.id, event_id)
    if not review:
        new_review = crud.create_review(
            session, user.profile.id, event_id, data
        )
        event.reviews.append(new_review)
        return event.reviews
    else:
        raise HTTPException(
            400,
            f"User #{user_id} has already made a review of the event #{event_id}!"
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
        "/users/{user_id}/reviews",
        response_model=list[ReviewEventList]
)
def list_user_reviews(
    session:Session, user_id:int, score:int|None=None
) -> list[Review]:
    """List reviews made by a user."""

    user = get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(404, f"User #{user_id} not found!")
    if score is not None:
        reviews = [
            review for review in user.profile.reviews
            if review.score == score
        ]
    else:
        reviews = user.profile.reviews
    return reviews



@review.get(
    "/events/{event_id}/users/{user_id}/reviews",
    response_model=ReviewRead
)
def get_review(
    session:Session, event_id:int, user_id:int
) -> Review:
    """get a user review for an event."""

    user = get_user_by_id(session, user_id)
    review = crud.get_review(session, event_id, user.profile.id)
    if not review:
        raise HTTPException(
            404,
            f"User #{user_id} has not made any reviews of the event #{event_id}!"
        )
    return review



@review.put(
    "/events/{event_id}/users/{user_id}/reviews",
    response_model=Review
)
def update_review(
    session:Session,
    event_id:int,
    user_id:int,
    data:ReviewUpdate
) -> Review:
    """Update a user review for an event."""

    user = get_user_by_id(session, user_id)
    review = crud.get_review(session, user.profile.id, event_id)
    if not review:
        raise HTTPException(
            404,
            f"User #{user_id} has not made any reviews of the event #{event_id}!"
        )
    review = crud.update_review(session, review, data)
    return review



@review.delete(
    "/events/{event_id}/users/{user_id}/reviews",
    status_code=204
)
def delete_review(
    session:Session, event_id:int, user_id:int, hard:bool=False
) -> None:
    """Delete a user review for a particular event."""

    event = get_event_by_id(session, event_id)
    user = get_user_by_id(session, user_id)
    if not event:
        raise HTTPException(404, f"Event #{event_id} not found!")
    if not user:
        raise HTTPException(404, f"User #{user_id} not found!")
    review = crud.get_review(session, event_id, user.profile.id)
    if review:
        crud.delete_review(session, review, hard)
    else:
        raise HTTPException(
            404,
            f"User #{user_id} has not made any reviews of the event #{event_id}!"
        )



# Path endpoints

path = APIRouter()


@path.get("/paths", response_model=dict)
def list_paths(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> dict:
    """List paths."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    total_records = crud.count_paths(session, filter_dict)
    current_page = (skip // limit) + 1 if limit else 1
    total_pages = (total_records + limit - 1) // limit if limit else 1
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    paths = crud.list_paths(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )

    return {
        "data": paths,
        "pagination": {
            "total_records": total_records,
            "per_page": limit,
            "current_page": current_page,
            "total_pages": total_pages,
            "next_page": next_page,
            "prev_page": prev_page
        }
    }



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
