"""
GET    /teams?skip=&limit=&location_id=  : list teams
POST   /teams                            : create team
GET    /teams/{team_id}                  : get team
PUT    /teams/{team_id}                  : update team
DELETE /teams/{team_id}?hard=            : delete team
GET    /teams/{team_id}/location    : get team's location
GET    /teams/{team_id}/members     : list team's members
GET    /teams/{team_id}/agreements  : list team's agreements
GET    /teams/{team_id}/events      : list team's events

GET    /locations?skip=&limit=&loc_type=&department_id=&is_capital=  : list locations
POST   /locations                                                    : create location
GET    /locations/{location_id}                                      : get location
PUT     /locations/{location_id}                                     : update location
DELETE  /locations/{location_id}?hard=                               : delete location
GET     /locations/{location_id}/department  : get location's department
GET     /locations/{location_id}/cities      : list location's cities
GET     /locations/{location_id}/team        : get location's team
GET     /locations/{location_id}/events      : list location's events
"""

from fastapi import APIRouter, HTTPException

from api.crud import teams as crud
from api.models.teams import Team, Location
from api.models.utils.enums import LocationType
from api.schemas.agreements import AgreementList
from api.schemas.events import EventList
from api.schemas.teams import (
    TeamCreate, TeamRead, TeamUpdate, TeamList,
    LocationCreate, LocationRead, LocationUpdate, LocationList)
from api.schemas.users import MemberList
from core.database import DBSession as Session



router = APIRouter()



# Team endpoints

@router.get("/teams", response_model=list[TeamList])
def list_teams(
    session:Session, skip:int=0, limit:int=10, location_id:int|None=None
) -> list[Team]:
    """List teams."""

    return crud.list_teams(session, skip, limit, location_id)



@router.post("/teams", response_model=TeamRead, status_code=201)
def create_team(session:Session, data:TeamCreate) -> Team:
    """Create a new team."""

    team = crud.get_team_by_name(session, data.name)
    if team:
        raise HTTPException(409, f"Team {data.name} already exists!")
    return crud.create_team(session, data)



@router.get("/teams/{team_id}", response_model=TeamRead)
def get_team(session:Session, team_id:int) -> Team:
    """Get a team by its ID."""

    team = crud.get_team_by_id(session, team_id)
    if not team:
        raise HTTPException(404, f"Team #{team_id} not found!")
    return team



@router.put("/teams/{team_id}", response_model=TeamRead)
def update_team(session:Session, team_id:int, data:TeamUpdate) -> Team:
    """Update a team."""

    team = crud.update_team(session, team_id, data)
    if not team:
        raise HTTPException(404, f"Team #{team_id} not found!")
    return team



@router.delete("/teams/{team_id}", status_code=204)
def delete_team(session:Session, team_id:int, hard:bool=False) -> None:
    """Delete a team by its ID."""

    team = crud.get_team_by_id(session, team_id)
    if not team:
        raise HTTPException(404, f"Team #{team_id} not found!")
    crud.delete_team(session, team_id, hard)



# Team relationship endpoints

@router.get("/teams/{team_id}/location", response_model=LocationRead)
def get_team_location(session:Session, team_id:int):
    """Get the location of a team."""

    team = crud.get_team_by_id(session, team_id)
    if not team:
        raise HTTPException(404, f"Team #{team_id} not found!")
    return team.location



@router.get("/teams/{team_id}/members", response_model=list[MemberList])
def list_team_members(session:Session, team_id:int):
    """Get the members of a team."""

    team = crud.get_team_by_id(session, team_id)
    if not team:
        raise HTTPException(404, f"Team #{team_id} not found!")
    return team.members



@router.get("/teams/{team_id}/events", response_model=list[EventList])
def list_team_events(session:Session, team_id:int):
    """Get the events of a team."""

    team = crud.get_team_by_id(session, team_id)
    if not team:
        raise HTTPException(404, f"Team #{team_id} not found!")
    return team.events



@router.get("/teams/{team_id}/agreements", response_model=list[AgreementList])
def list_team_agreements(session:Session, team_id:int):
    """Get the agreements of a team."""

    team = crud.get_team_by_id(session, team_id)
    if not team:
        raise HTTPException(404, f"Team #{team_id} not found!")
    return team.agreements



# Location endpoints

@router.get("/locations", response_model=list[LocationList])
def list_locations(
    session:Session,
    skip:int=0,
    limit:int=10,
    loc_type:LocationType|None=None,
    department_id:int|None=None,
    is_capital:bool|None=None
) -> list[Location]:
    """List locations."""

    return crud.list_locations(
        session, skip, limit, loc_type, department_id, is_capital
    )



@router.post("/locations", response_model=LocationRead, status_code=201)
def create_location(session:Session, data:LocationCreate) -> Location:
    """Create a new location."""

    location = crud.get_location_by_name(session, data.name)
    if location:
        raise HTTPException(409, f"Location {data.name} already exists!")
    return crud.create_location(session, data)



@router.get("/locations/{location_id}", response_model=LocationRead,)
def get_location(session:Session, location_id:int) -> Location:
    """Get a location by its ID."""

    location = crud.get_location_by_id(session, location_id)
    if not location:
        raise HTTPException(404, f"Location #{location_id} not found!")
    return location



@router.put("/locations/{location_id}",response_model=LocationRead,)
def update_location(
    session:Session, location_id:int, data:LocationUpdate
) -> Location:
    """Update a location."""

    location = crud.update_location(session, location_id, data)
    if not location:
        raise HTTPException(404, f"Location #{location_id} not found!")
    return location



@router.delete("/locations/{location_id}", status_code=204)
def delete_location(
    session:Session, location_id:int, hard:bool|None=None
) -> None:
    """Delete a location by its ID."""

    location = crud.get_location_by_id(session, location_id)
    if not location:
        raise HTTPException(404, f"Location #{location_id} not found!")
    crud.delete_location(session, location_id, hard)



# Location relationship endpoints

@router.get("/locations/{location_id}/department", response_model=LocationRead)
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



@router.get(
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



@router.get("/locations/{location_id}/team", response_model=TeamRead)
def get_location_team(session:Session, location_id:int):
    """Get the team of a location."""

    location = crud.get_location_by_id(session, location_id)
    if not location:
        raise HTTPException(404, f"Location #{location_id} not found!")
    return location.team



@router.get("/locations/{location_id}/events", response_model=list[EventList])
def list_location_events(session:Session, location_id:int):
    """Get the events of a location."""

    location = crud.get_location_by_id(session, location_id)
    if not location:
        raise HTTPException(404, f"Location #{location_id} not found!")
    return location.events
