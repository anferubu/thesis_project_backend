from datetime import date
import io

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, StreamingResponse

from api.crud import users as crud
from api.crud.utils import parse_filter_param, parse_sort_param
from api.models.users import Brand, Motorcycle, Role, User
from api.routers.utils import get_membership_card
from api.schemas.users import (
    BrandCreate, BrandList, BrandRead, BrandUpdate,
    MotorcycleCreate, MotorcycleList, MotorcycleRead, MotorcycleUpdate,
    RoleCreate, RoleList, RoleRead, RoleUpdate,
    UserList, UserRead, UserUpdate)
from core.database import DBSession as Session



role = APIRouter()



# Role endpoints

@role.get("/roles", response_model=dict)
def list_roles(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> dict:
    """List roles."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    total_records = crud.count_roles(session, filter_dict)
    current_page = (skip // limit) + 1 if limit else 1
    total_pages = (total_records + limit - 1) // limit if limit else 1
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    roles = crud.list_roles(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )

    return {
        "data": roles,
        "pagination": {
            "total_records": total_records,
            "per_page": limit,
            "current_page": current_page,
            "total_pages": total_pages,
            "next_page": next_page,
            "prev_page": prev_page
        }
    }



@role.post("/roles", response_model=RoleRead, status_code=201)
def create_role(session:Session, data:RoleCreate) -> Role:
    """Create a new role."""

    role = crud.get_role_by_name(session, data.name)
    if role:
        raise HTTPException(409, f"Role {data.name} already exists!")
    return crud.create_role(session, data)



@role.get("/roles/{role_id}", response_model=RoleRead)
def get_role(session:Session, role_id:int) -> Role:
    """Get a role by its ID."""

    role = crud.get_role_by_id(session, role_id)
    if not role:
        raise HTTPException(404, f"Role #{role_id} not found!")
    return role



@role.put("/roles/{role_id}", response_model=RoleRead)
def update_role(session:Session, role_id:int, data:RoleUpdate) -> Role:
    """Update a role."""

    role = crud.update_role(session, role_id, data)
    if not role:
        raise HTTPException(404, f"Role #{role_id} not found!")
    return role



@role.delete("/roles/{role_id}", status_code=204)
def delete_role(
    session:Session, role_id:int, hard:bool=False
) -> None:
    """Delete a role by its ID."""

    role = crud.get_role_by_id(session, role_id)
    if not role:
        raise HTTPException(404, f"Role #{role_id} not found!")
    crud.delete_role(session, role_id, hard)



# Role relationship endpoints

@role.get("/roles/{role_id}/users", response_model=list[UserList])
def list_role_users(session:Session, role_id:int):
    """Get the users with a role."""

    role = crud.get_role_by_id(session, role_id)
    if not role:
        raise HTTPException(404, f"Role #{role_id} not found!")
    return role.users



# Motorcycle endpoints

motorcycle = APIRouter()


@motorcycle.get("/motorcycles", response_model=dict)
def list_motorcycles(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> dict:
    """List motorcycles."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    total_records = crud.count_motorcycles(session, filter_dict)
    current_page = (skip // limit) + 1 if limit else 1
    total_pages = (total_records + limit - 1) // limit if limit else 1
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    motorcycles = crud.list_motorcycles(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )

    return {
        "data": motorcycles,
        "pagination": {
            "total_records": total_records,
            "per_page": limit,
            "current_page": current_page,
            "total_pages": total_pages,
            "next_page": next_page,
            "prev_page": prev_page
        }
    }



@motorcycle.post(
    "/motorcycles", response_model=MotorcycleRead, status_code=201
)
def create_motorcycle(session:Session, data:MotorcycleCreate) -> Motorcycle:
    """Create a new motorcycle."""

    motorcycle = crud.get_motorcycle_by_license_plate(
        session, data.license_plate
    )
    brand = crud.get_brand_by_id(session, data.brand_id)
    owner = crud.get_user_by_id(session, data.owner_id)
    if motorcycle:
        raise HTTPException(
            409, f"Motorcycle {data.license_plate} already exists!"
        )
    if not brand:
        raise HTTPException(404, f"Brand #{data.brand_id} not found!")
    if not owner:
        raise HTTPException(404, f"User #{data.owner_id} not found!")
    data.owner_id = owner.profile.id
    return crud.create_motorcycle(session, data)



@motorcycle.get("/motorcycles/{motorcycle_id}", response_model=MotorcycleRead)
def get_motorcycle(session:Session, motorcycle_id:int) -> Motorcycle:
    """Get a motorcycle by its ID."""

    motorcycle = crud.get_motorcycle_by_id(session, motorcycle_id)
    if not motorcycle:
        raise HTTPException(404, f"Motorcycle #{motorcycle_id} not found!")
    return motorcycle



@motorcycle.put("/motorcycles/{motorcycle_id}", response_model=MotorcycleRead)
def update_motorcycle(
    session:Session, motorcycle_id:int, data:MotorcycleUpdate
) -> Motorcycle:
    """Update a motorcycle."""

    motorcycle = crud.update_motorcycle(session, motorcycle_id, data)
    if not motorcycle:
        raise HTTPException(404, f"Motorcycle #{motorcycle_id} not found!")
    return motorcycle



@motorcycle.delete("/motorcycles/{motorcycle_id}", status_code=204)
def delete_motorcycle(
    session:Session, motorcycle_id:int, hard:bool=False
) -> None:
    """Delete a motorcycle by its ID."""

    motorcycle = crud.get_motorcycle_by_id(session, motorcycle_id)
    if not motorcycle:
        raise HTTPException(404, f"Motorcycle #{motorcycle_id} not found!")
    crud.delete_motorcycle(session, motorcycle_id, hard)



# Motorcycle relationship endpoints

@motorcycle.get("/motorcycles/{motorcycle_id}/brand", response_model=BrandRead)
def get_motorcycle_brand(session:Session, motorcycle_id:int):
    """Get the brand of a motorcycle."""

    motorcycle = crud.get_motorcycle_by_id(session, motorcycle_id)
    if not motorcycle:
        raise HTTPException(404, f"Motorcycle #{motorcycle_id} not found!")
    return motorcycle.brand



@motorcycle.get("/motorcycles/{motorcycle_id}/owner", response_model=UserRead)
def get_motorcycle_owner(session:Session, motorcycle_id:int):
    """Get the owner of a motorcycle."""

    motorcycle = crud.get_motorcycle_by_id(session, motorcycle_id)
    if not motorcycle:
        raise HTTPException(404, f"Motorcycle #{motorcycle_id} not found!")
    return motorcycle.owner.user



# Brand endpoints

brand = APIRouter()


@brand.get("/brands", response_model=dict)
def list_brands(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> dict:
    """List brands."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    total_records = crud.count_brands(session, filter_dict)
    current_page = (skip // limit) + 1 if limit else 1
    total_pages = (total_records + limit - 1) // limit if limit else 1
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    brands = crud.list_brands(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )

    return {
        "data": brands,
        "pagination": {
            "total_records": total_records,
            "per_page": limit,
            "current_page": current_page,
            "total_pages": total_pages,
            "next_page": next_page,
            "prev_page": prev_page
        }
    }



@brand.post("/brands", response_model=BrandRead, status_code=201)
def create_brand(session:Session, data:BrandCreate) -> Brand:
    """Create a new brand."""

    brand = crud.get_brand_by_name(session, data.name)
    if brand:
        raise HTTPException(409, f"Brand {data.name} already exists!")
    return crud.create_brand(session, data)



@brand.get("/brands/{brand_id}", response_model=BrandRead)
def get_brand(session:Session, brand_id:int) -> Brand:
    """Get a brand by its ID."""

    brand = crud.get_brand_by_id(session, brand_id)
    if not brand:
        raise HTTPException(404, f"Brand #{brand_id} not found!")
    return brand



@brand.put("/brands/{brand_id}", response_model=BrandRead)
def update_brand(session:Session, brand_id:int, data:BrandUpdate) -> Brand:
    """Update a brand."""

    brand = crud.update_brand(session, brand_id, data)
    if not brand:
        raise HTTPException(404, f"Brand #{brand_id} not found!")
    return brand



@brand.delete("/brands/{brand_id}", status_code=204)
def delete_brand(session:Session, brand_id:int, hard:bool=False) -> None:
    """Delete a brand by its ID."""

    brand = crud.get_brand_by_id(session, brand_id)
    if not brand:
        raise HTTPException(404, f"Brand #{brand_id} not found!")
    crud.delete_brand(session, brand_id, hard)



# Brand relationship endpoints

@brand.get(
    "/brands/{brand_id}/motorcycles", response_model=list[MotorcycleList]
)
def list_brand_motorcycles(session:Session, brand_id:int):
    """Get the motorcycles of a brand."""

    brand = crud.get_brand_by_id(session, brand_id)
    if not brand:
        raise HTTPException(404, f"Brand #{brand_id} not found!")
    return brand.motorcycles



# User endpoints

user = APIRouter()


@user.get("/users", response_model=dict)
def list_users(
    session:Session,
    skip:int=0,
    limit:int=100,
    sort:str|None=None,
    filter:str|None=None
) -> dict:
    """List users."""

    sort_dict = parse_sort_param(sort) if sort else None
    filter_dict = parse_filter_param(filter) if filter else None

    total_records = crud.count_users(session, filter_dict)
    current_page = (skip // limit) + 1 if limit else 1
    total_pages = (total_records + limit - 1) // limit if limit else 1
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    users = crud.list_users(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort_dict,
        filter=filter_dict
    )

    return {
        "data": users,
        "pagination": {
            "total_records": total_records,
            "per_page": limit,
            "current_page": current_page,
            "total_pages": total_pages,
            "next_page": next_page,
            "prev_page": prev_page
        }
    }



@user.get("/users/{user_id}", response_model=UserRead)
def get_user(session:Session, user_id:int) -> User:
    """Get a user by its ID."""

    user = crud.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(404, f"User #{user_id} not found!")
    return user



@user.put("/users/{user_id}", response_model=UserRead)
def update_user(
    session:Session, user_id:int, data:UserUpdate
) -> User:
    """Update a user."""

    user = crud.update_user(session, user_id, data)
    if not user:
        raise HTTPException(404, f"User #{user_id} not found!")
    return user



@user.delete("/users/{user_id}", status_code=204)
def delete_user(
    session:Session, user_id:int, hard:bool=False
) -> None:
    """Delete a user by its ID."""

    user = crud.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(404, f"User #{user_id} not found!")
    crud.delete_user(session, user_id, hard)



@user.get("/users/{user_id}/motorcycles", response_model=list[MotorcycleRead])
def get_user_motorcycles(session:Session, user_id:int) -> Motorcycle:
    """Get the user's motorcycles by his ID."""

    user = crud.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(404, f"User #{user_id} not found!")
    return user.profile.motorcycles


# Membershipt card endpoints

membership = APIRouter()


@membership.get("/users/{user_id}/membership-card")
def generate_membership_card(session:Session, user_id:int, format:str="PNG"):
    """Get the membership card of a user."""

    user = crud.get_user_by_id(session, user_id)
    photo = user.profile.photo
    if not user:
        raise HTTPException(404, f"User #{user_id} not found!")
    data = {
        "name": user.profile.first_name,
        "surname": user.profile.last_name,
        "team": user.profile.team.name,
        "role": user.role.name,
        "doc_type": user.profile.document_type.name,
        "doc_number": user.profile.document_number,
        "rh": user.profile.rh.value,
        "location": user.profile.team.location.name,
        "telephone": user.profile.telephone,
        "output_format": format,
    }
    if photo is not None:
        data["photo_path"] = photo
    card = get_membership_card(**data)
    file = io.BytesIO(card)
    if format.upper() == "PDF":
        headers = {"Content-Disposition": 'attachment; filename="membership_card.pdf"'}
        return StreamingResponse(file, headers=headers, media_type="application/pdf")
    else:
        return StreamingResponse(file, media_type="image/png")



# Birthdates endpoints

birthdate = APIRouter()


@birthdate.get("/users/birthdates/today", response_model=list[UserList])
def list_birthdays_today(session:Session) -> list[User]:
    """List users whose birthday is today."""

    birthdays_today = crud.list_users_birthday_is_today(session)
    return birthdays_today



@birthdate.get("/users/birthdates", response_model=list[UserList])
def list_birthdays_by_date(
    session:Session,
    date:date|None=None,
    start_date:date|None=None,
    end_date:date|None=None,
) -> list[User]:
    """List users whose birthday is on a specific date or within a range."""

    if date:
        users = crud.list_users_by_birthdate(session, date)
    elif start_date and end_date:
        users = crud.list_users_by_birthdate_range(
            session, start_date, end_date
        )
    else:
        raise HTTPException(
            400, "You must provide either 'date' or both 'start_date' and 'end_date' parameters."
        )
    return users
