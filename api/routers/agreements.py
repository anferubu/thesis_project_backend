from fastapi import APIRouter, HTTPException

from api.crud import agreements as crud
from api.crud.teams import get_team_by_id
from api.crud.utils import parse_filter_param, parse_sort_param
from api.dependencies.roles import roles_required
from api.models.agreements import Agreement, Company
from api.schemas.agreements import (
    AgreementCreate, AgreementRead, AgreementUpdate, AgreementList,
    CompanyCreate, CompanyRead, CompanyUpdate, CompanyList)
from api.schemas.teams import TeamList, TeamAdd
from core.database import DBSession as Session



agreement = APIRouter()



# Agreement endpoints

@agreement.get(
    "/agreements",
    response_model=dict,
)
def list_agreements(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> dict:
    """List agreements."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    total_records = crud.count_agreements(session, filter_dict)
    current_page = (skip // limit) + 1 if limit else 1
    total_pages = (total_records + limit - 1) // limit if limit else 1
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    agreements = crud.list_agreements(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )

    return {
        "data": agreements,
        "pagination": {
            "total_records": total_records,
            "per_page": limit,
            "current_page": current_page,
            "total_pages": total_pages,
            "next_page": next_page,
            "prev_page": prev_page
        }
    }



@agreement.post("/agreements", response_model=AgreementRead, status_code=201)
def create_agreement(session:Session, data:AgreementCreate) -> Agreement:
    """Create a new agreement."""

    agreement = crud.get_agreement_by_name(session, data.name)
    if agreement:
        raise HTTPException(409, f"Agreement {data.name} already exists!")
    return crud.create_agreement(session, data)



@agreement.get("/agreements/{agreement_id}", response_model=AgreementRead)
def get_agreement(session:Session, agreement_id:int) -> Agreement:
    """Get an agreement by its ID."""

    agreement = crud.get_agreement_by_id(session, agreement_id)
    if not agreement:
        raise HTTPException(404, f"Agreement #{agreement_id} not found!")
    return agreement



@agreement.put("/agreements/{agreement_id}", response_model=AgreementRead)
def update_agreement(
    session:Session, agreement_id:int, data:AgreementUpdate
) -> Agreement:
    """Update an agreement."""

    agreement = crud.update_agreement(session, agreement_id, data)
    if not agreement:
        raise HTTPException(404, f"Agreement #{agreement_id} not found!")
    return agreement



@agreement.delete("/agreements/{agreement_id}", status_code=204)
def delete_agreement(
    session:Session, agreement_id:int, hard:bool=False
) -> None:
    """Delete an agreement by its ID."""

    agreement = crud.get_agreement_by_id(session, agreement_id)
    if not agreement:
        raise HTTPException(404, f"Agreement #{agreement_id} not found!")
    crud.delete_agreement(session, agreement_id, hard)



# Agreement relationship endpoints

@agreement.get(
    "/agreements/{agreement_id}/company", response_model=CompanyRead
)
def get_agreement_company(session:Session, agreement_id:int):
    """Get the company from an agreement."""

    agreement = crud.get_agreement_by_id(session, agreement_id)
    if not agreement:
        raise HTTPException(404, f"Agreement #{agreement_id} not found!")
    return agreement.company



@agreement.get(
    "/agreements/{agreement_id}/teams", response_model=list[TeamList]
)
def list_agreement_teams(session:Session, agreement_id:int):
    """Get the teams from an agreement."""

    agreement = crud.get_agreement_by_id(session, agreement_id)
    if not agreement:
        raise HTTPException(404, f"Agreement #{agreement_id} not found!")
    return agreement.teams



@agreement.post(
    "/agreements/{agreement_id}/teams", response_model=list[TeamList]
)
def add_team_to_agreement(session:Session, agreement_id:int, data:TeamAdd):
    """Add a team to an agreement."""

    agreement = crud.get_agreement_by_id(session, agreement_id)
    team = get_team_by_id(session, data.id)
    if not agreement:
        raise HTTPException(404, f"Agreement #{agreement_id} not found!")
    if not team:
        raise HTTPException(404, f"Team #{data.id} not found!")
    teams = crud.add_team_to_agreement(session, agreement_id, data.id)
    return teams



@agreement.delete(
    "/agreements/{agreement_id}/teams/{team_id}", status_code=204
)
def remove_team_from_agreement(session:Session, agreement_id:int, team_id:int):
    """Remove a team from an agreement."""

    agreement = crud.get_agreement_by_id(session, agreement_id)
    team = get_team_by_id(session, team_id)
    if not agreement:
        raise HTTPException(404, f"Agreement #{agreement_id} not found!")
    if not team:
        raise HTTPException(404, f"Team #{team_id} not found!")
    if team not in agreement.teams:
        raise HTTPException(404, f"Team #{team_id} not found in agreement #{agreement_id}!")
    crud.remove_team_from_agreement(session, agreement_id, team_id)



# Company endpoints

company = APIRouter()


@company.get("/companies", response_model=dict)
def list_companies(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> dict:
    """List companies."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    total_records = crud.count_companies(session, filter_dict)
    current_page = (skip // limit) + 1 if limit else 1
    total_pages = (total_records + limit - 1) // limit if limit else 1
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    companies = crud.list_companies(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )

    return {
        "data": companies,
        "pagination": {
            "total_records": total_records,
            "per_page": limit,
            "current_page": current_page,
            "total_pages": total_pages,
            "next_page": next_page,
            "prev_page": prev_page
        }
    }



@company.post("/companies", response_model=CompanyRead, status_code=201)
def create_company(session:Session, data:CompanyCreate) -> Company:
    """Create a new company."""

    company = crud.get_company_by_name(session, data.name)
    if company:
        raise HTTPException(409, f"Company {data.name} already exists!")
    return crud.create_company(session, data)



@company.get("/companies/{company_id}", response_model=CompanyRead)
def get_company(session:Session, company_id:int) -> Company:
    """Get a company by its ID."""

    company = crud.get_company_by_id(session, company_id)
    if not company:
        raise HTTPException(404, f"Company #{company_id} not found!")
    return company



@company.put("/companies/{company_id}", response_model=CompanyRead)
def update_company(
    session:Session, company_id:int, data:CompanyUpdate
) -> Company:
    """Update a company."""

    company = crud.update_company(session, company_id, data)
    if not company:
        raise HTTPException(404, f"Company #{company_id} not found!")
    return company



@company.delete("/companies/{company_id}", status_code=204)
def delete_company(
    session:Session, company_id:int, hard:bool=False
) -> None:
    """Delete a company by its ID."""

    company = crud.get_company_by_id(session, company_id)
    if not company:
        raise HTTPException(404, f"Company #{company_id} not found!")
    crud.delete_company(session, company_id, hard)



# Company relationship endpoints

@company.get(
    "/companies/{company_id}/agreements", response_model=list[AgreementList]
)
def get_company_agreements(session:Session, company_id:int):
    """Get the agreements from a company."""

    company = crud.get_company_by_id(session, company_id)
    if not company:
        raise HTTPException(404, f"Company #{company_id} not found!")
    return company.agreements
