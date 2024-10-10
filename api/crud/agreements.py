from sqlalchemy import func
from sqlmodel import Session, select

from api.crud.utils import apply_filters, apply_sorting
from api.models.agreements import Agreement, Company
from api.models.teams import Team
from api.schemas.agreements import (
    AgreementCreate, AgreementUpdate, CompanyCreate, CompanyUpdate)



# Agreement model CRUD

def create_agreement(session:Session, data:AgreementCreate) -> Agreement:
    """Create an agreement."""

    new_agreement = Agreement.model_validate(data)
    session.add(new_agreement)
    session.commit()
    session.refresh(new_agreement)
    return new_agreement



def get_agreement_by_id(session:Session, agreement_id:int) -> Agreement|None:
    """Get an agreement by its ID."""

    agreement = session.get(Agreement, agreement_id)
    return agreement if agreement and not agreement.deleted else None



def get_agreement_by_name(session:Session, name:str) -> Agreement|None:
    """Get an agreement by its name."""

    query = select(Agreement).where(
        func.lower(Agreement.name) == name.lower(), Agreement.deleted == False
    )
    return session.exec(query).first()



def list_agreements(
    session:Session,
    skip:int|None=None,
    limit:int|None=None,
    sort: dict[str, str]|None = None,
    filter: dict[str, any]|None = None,
) -> list[Agreement]:
    """List agreements."""

    query = select(Agreement).where(Agreement.deleted == False)
    if filter:
        query = apply_filters(query, Agreement, filter)
    if sort:
        query = apply_sorting(query, Agreement, sort)
    if skip:
        query = query.offset(skip)
    if limit:
        query = query.limit(limit)
    return session.exec(query).all()



def count_agreements(session:Session, filter:dict[str, any]|None=None) -> int:
    query = select(func.count(Agreement.id)).where(Agreement.deleted == False)
    if filter:
        query = apply_filters(query, Agreement, filter)
    return session.exec(query).one()



def update_agreement(
        session:Session, agreement_id:int, data:AgreementUpdate
) -> Agreement|None:
    """Update an agreement."""

    agreement = session.get(Agreement, agreement_id)
    if agreement:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(agreement, field, value)
        session.commit()
        session.refresh(agreement)
    return agreement



def delete_agreement(
        session:Session, agreement_id:int, hard:bool=False
) -> None:
    """Delete an agreement."""

    agreement = session.get(Agreement, agreement_id)
    if agreement:
        if hard:
            session.delete(agreement)
            session.commit()
        else:
            agreement.deleted = True
            session.commit()
            session.refresh(agreement)



# Agreement relationship CRUD

def add_team_to_agreement(
        session:Session, agreement_id:int, team_id:int
) -> list[Team]:
    """Add a team to an agreement."""

    agreement = session.get(Agreement, agreement_id)
    team = session.get(Team, team_id)
    if agreement:
        agreement.teams.append(team)
        session.commit()
        session.refresh(agreement)
    return agreement.teams



def remove_team_from_agreement(
        session:Session, agreement_id:int, team_id:int
) -> list[Team]:
    """Remove a team from an agreement."""

    agreement = session.get(Agreement, agreement_id)
    if agreement:
        agreement.teams = [
            team for team in agreement.teams if team.id != team_id
        ]
        session.commit()
        session.refresh(agreement)
    return agreement.teams



# Company model CRUD

def create_company(session:Session, data:CompanyCreate) -> Company:
    """Create a new company."""

    new_company = Company.model_validate(data)
    session.add(new_company)
    session.commit()
    session.refresh(new_company)
    return new_company



def get_company_by_id(session:Session, company_id:int) -> Company|None:
    """Get a company by its ID."""

    company = session.get(Company, company_id)
    return company if company and not company.deleted else None



def get_company_by_name(session:Session, name:str) -> Company|None:
    """Get a company by its name."""

    query = select(Company).where(
        Company.name == name, Company.deleted == False
    )
    return session.exec(query).first()



def list_companies(
    session:Session,
    skip:int|None=None,
    limit:int|None=None,
    sort: dict[str, str]|None = None,
    filter: dict[str, any]|None = None
) -> list[Company]:
    """List companies."""

    query = select(Company).where(Company.deleted == False)
    if filter:
        query = apply_filters(query, Company, filter)
    if sort:
        query = apply_sorting(query, Company, sort)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return session.exec(query).all()



def count_companies(session:Session, filter:dict[str, any]|None=None) -> int:
    query = select(func.count(Company.id)).where(Company.deleted == False)
    if filter:
        query = apply_filters(query, Company, filter)
    return session.exec(query).one()



def update_company(
    session:Session, company_id:int, data:CompanyUpdate
) -> Company|None:
    """Update a company."""

    company = session.get(Company, company_id)
    if company:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(company, field, value)
        session.commit()
        session.refresh(company)
    return company



def delete_company(session:Session, company_id:int, hard:bool=False) -> None:
    """Delete a company."""

    company = session.get(Company, company_id)
    if company:
        if hard:
            session.delete(company)
            session.commit()
        else:
            company.deleted = True
            session.commit()
            session.refresh(company)
