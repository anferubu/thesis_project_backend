from sqlmodel import Session, select

from api.models.teams import Location, Team
from api.models.utils.enums import LocationType
from api.schemas.teams import (
    TeamCreate, TeamUpdate, LocationCreate, LocationUpdate)



# Team model CRUD

def create_team(session:Session, data:TeamCreate) -> Team:
    """Create a team."""

    new_team = Team.model_validate(data)
    session.add(new_team)
    session.commit()
    session.refresh(new_team)
    return new_team



def get_team_by_id(session:Session, team_id:int) -> Team|None:
    """Get a team by its ID."""

    team = session.get(Team, team_id)
    return team if team and not team.deleted else None



def get_team_by_name(session:Session, name:str) -> Team|None:
    """Get a team by its name."""

    query = select(Team).where(Team.name == name, Team.deleted == False)
    return session.exec(query).first()



def list_teams(
        session:Session,
        skip:int|None=None,
        limit:int|None=None,
        location_id:int|None=None
) -> list[Team]:
    """List teams."""

    query = select(Team).where(Team.deleted == False)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    if location_id is not None:
        query = query.where(Team.location_id == location_id)
    return session.exec(query).all()



def update_team(session:Session, team_id:int, data:TeamUpdate) -> Team|None:
    """Update a team."""

    team = session.get(Team, team_id)
    if team:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(team, field, value)
        session.commit()
        session.refresh(team)
    return team



def delete_team(session:Session, team_id:int, hard:bool=False) -> None:
    """Delete a team."""

    team = session.get(Team, team_id)
    if team:
        if hard:
            session.delete(team)
            session.commit()
        else:
            team.deleted = True
            session.commit()
            session.refresh(team)



# Team model relationships CRUD
# These functionalities are already implemented in the Agreement CRUD



# Location model CRUD

def create_location(session:Session, data:LocationCreate) -> Location:
    """Create a new location."""

    new_location = Location.model_validate(data)
    session.add(new_location)
    session.commit()
    session.refresh(new_location)
    return new_location



def get_location_by_id(session:Session, location_id:int) -> Location|None:
    """Get a location by its ID."""

    location = session.get(Location, location_id)
    return location if location and not location.deleted else None



def get_location_by_name(session:Session, name:str) -> Location|None:
    """Get a location by its name."""

    query = select(Location).where(
        Location.name == name, Location.deleted == False
    )
    return session.exec(query).first()



def list_locations(
        session:Session,
        skip:int|None=None,
        limit:int|None=None,
        loc_type:LocationType|None=None,
        department_id:int|None=None,
        is_capital:bool|None=None
) -> list[Location]:
    """List locations."""

    query = select(Location).where(Location.deleted == False)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    if loc_type is not None:
        query = query.where(Location.type == loc_type)
    if department_id is not None:
        query = query.where(Location.department_id == department_id)
    if is_capital is not None:
        query = query.where(Location.is_capital == is_capital)
    return session.exec(query).all()



def update_location(
        session:Session, location_id:int, data:LocationUpdate
) -> Location|None:
    """Update a location."""

    location = session.get(Location, location_id)
    if location:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(location, field, value)
        session.commit()
        session.refresh(location)
    return location



def delete_location(session:Session, location_id:int, hard:bool=False) -> None:
    """Delete a location."""

    location = session.get(Location, location_id)
    if location:
        if hard:
            session.delete(location)
            session.commit()
        else:
            location.deleted = True
            session.commit()
            session.refresh(location)
    return location
