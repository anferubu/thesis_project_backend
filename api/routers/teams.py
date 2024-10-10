from fastapi import APIRouter, HTTPException

from api.crud import teams as crud
from api.crud.utils import parse_filter_param, parse_sort_param
from api.models.teams import Team, Location
from api.models.utils.enums import LocationType
from api.schemas.agreements import AgreementList
from api.schemas.events import EventList
from api.schemas.teams import (
    TeamCreate, TeamRead, TeamUpdate, TeamList,
    LocationCreate, LocationRead, LocationUpdate, LocationList)
from api.schemas.users import UserList
from core.database import DBSession as Session



team = APIRouter()



# Team endpoints

@team.get("/teams", response_model=dict)
def list_teams(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> dict:
    """List teams."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    total_records = crud.count_teams(session, filter_dict)
    current_page = (skip // limit) + 1 if limit else 1
    total_pages = (total_records + limit - 1) // limit if limit else 1
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    teams = crud.list_teams(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )

    return {
        "data": teams,
        "pagination": {
            "total_records": total_records,
            "per_page": limit,
            "current_page": current_page,
            "total_pages": total_pages,
            "next_page": next_page,
            "prev_page": prev_page
        }
    }



@team.post("/teams", response_model=TeamRead, status_code=201)
def create_team(session:Session, data:TeamCreate) -> Team:
    """Create a new team."""

    team = crud.get_team_by_name(session, data.name)
    location = crud.get_location_by_id(session, data.location_id)
    if team:
        raise HTTPException(409, f"Team {data.name} already exists!")
    if not location:
        raise HTTPException(404, f"Location #{data.location_id} not found!")
    return crud.create_team(session, data)



@team.get("/teams/{team_id}", response_model=TeamRead)
def get_team(session:Session, team_id:int) -> Team:
    """Get a team by its ID."""

    team = crud.get_team_by_id(session, team_id)
    if not team:
        raise HTTPException(404, f"Team #{team_id} not found!")
    return team



@team.put("/teams/{team_id}", response_model=TeamRead)
def update_team(session:Session, team_id:int, data:TeamUpdate) -> Team:
    """Update a team."""

    team = crud.update_team(session, team_id, data)
    if not team:
        raise HTTPException(404, f"Team #{team_id} not found!")
    return team



@team.delete("/teams/{team_id}", status_code=204)
def delete_team(session:Session, team_id:int, hard:bool=False) -> None:
    """Delete a team by its ID."""

    team = crud.get_team_by_id(session, team_id)
    if not team:
        raise HTTPException(404, f"Team #{team_id} not found!")
    crud.delete_team(session, team_id, hard)



# Team relationship endpoints

@team.get("/teams/{team_id}/location", response_model=LocationRead)
def get_team_location(session:Session, team_id:int):
    """Get the location of a team."""

    team = crud.get_team_by_id(session, team_id)
    if not team:
        raise HTTPException(404, f"Team #{team_id} not found!")
    return team.location



@team.get("/teams/{team_id}/users", response_model=list[UserList])
def list_team_users(session:Session, team_id:int):
    """Get the users of a team."""

    team = crud.get_team_by_id(session, team_id)
    if not team:
        raise HTTPException(404, f"Team #{team_id} not found!")
    users = [profile.user for profile in team.members]
    return users



@team.get("/teams/{team_id}/events", response_model=list[EventList])
def list_team_events(session:Session, team_id:int):
    """Get the events of a team."""

    team = crud.get_team_by_id(session, team_id)
    if not team:
        raise HTTPException(404, f"Team #{team_id} not found!")
    return team.events



@team.get("/teams/{team_id}/agreements", response_model=list[AgreementList])
def list_team_agreements(session:Session, team_id:int):
    """Get the agreements of a team."""

    team = crud.get_team_by_id(session, team_id)
    if not team:
        raise HTTPException(404, f"Team #{team_id} not found!")
    return team.agreements



# Location endpoints

location = APIRouter()


@location.get("/locations", response_model=dict)
def list_locations(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> dict:
    """List locations."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    total_records = crud.count_locations(session, filter_dict)
    current_page = (skip // limit) + 1 if limit else 1
    total_pages = (total_records + limit - 1) // limit if limit else 1
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    locations = crud.list_locations(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )

    return {
        "data": locations,
        "pagination": {
            "total_records": total_records,
            "per_page": limit,
            "current_page": current_page,
            "total_pages": total_pages,
            "next_page": next_page,
            "prev_page": prev_page
        }
    }



@location.post("/locations", response_model=LocationRead, status_code=201)
def create_location(session:Session, data:LocationCreate) -> Location:
    """Create a new location."""

    location = crud.get_location_by_name(session, data.name)
    department = crud.get_location_by_id(session, data.department_id)
    if location:
        raise HTTPException(409, f"Location {data.name} already exists!")
    if not department:
        raise HTTPException(404, f"Department #{data.department_id} not found!")
    if department.type != LocationType.DEPARTMENT:
        raise HTTPException(
            409, f"Location #{data.department_id} is not a department!"
        )
    return crud.create_location(session, data)



@location.get("/locations/{location_id}", response_model=LocationRead,)
def get_location(session:Session, location_id:int) -> Location:
    """Get a location by its ID."""

    location = crud.get_location_by_id(session, location_id)
    if not location:
        raise HTTPException(404, f"Location #{location_id} not found!")
    return location



@location.put("/locations/{location_id}",response_model=LocationRead,)
def update_location(
    session:Session, location_id:int, data:LocationUpdate
) -> Location:
    """Update a location."""

    location = crud.update_location(session, location_id, data)
    if not location:
        raise HTTPException(404, f"Location #{location_id} not found!")
    return location



@location.delete("/locations/{location_id}", status_code=204)
def delete_location(
    session:Session, location_id:int, hard:bool|None=None
) -> None:
    """Delete a location by its ID."""

    location = crud.get_location_by_id(session, location_id)
    if not location:
        raise HTTPException(404, f"Location #{location_id} not found!")
    crud.delete_location(session, location_id, hard)



# Location relationship endpoints

@location.get(
    "/locations/{location_id}/department", response_model=LocationRead
)
def get_location_department(session:Session, location_id:int):
    """Get the department of a location."""

    location = crud.get_location_by_id(session, location_id)
    if not location:
        raise HTTPException(404, f"Location #{location_id} not found!")
    if location.type == LocationType.DEPARTMENT:
        raise HTTPException(
            409, f"The location #{location_id} is already a department!"
        )
    return location.department



@location.get(
    "/locations/{location_id}/cities", response_model=list[LocationList]
)
def list_location_cities(session:Session, location_id:int):
    """Get the cities of a department."""

    location = crud.get_location_by_id(session, location_id)
    if not location:
        raise HTTPException(404, f"Location #{location_id} not found!")
    if location.type == LocationType.CITY:
        raise HTTPException(
            409, f"Location #{location_id} is not a department!"
        )
    return location.cities



@location.get("/locations/{location_id}/team", response_model=TeamRead)
def get_location_team(session:Session, location_id:int):
    """Get the team of a location."""

    location = crud.get_location_by_id(session, location_id)
    if not location:
        raise HTTPException(404, f"Location #{location_id} not found!")
    return location.team



@location.get(
    "/locations/{location_id}/events", response_model=list[EventList]
)
def list_location_events(session:Session, location_id:int):
    """Get the events of a location."""

    location = crud.get_location_by_id(session, location_id)
    if not location:
        raise HTTPException(404, f"Location #{location_id} not found!")
    return location.events
