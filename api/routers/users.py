from fastapi import APIRouter, HTTPException

from api.crud import users as crud
from api.models.users import Brand, Member, Motorcycle, Role, User
from api.models.utils.enums import UserStatus, GenderType, DocumentType, RHType
from api.schemas.users import (
    BrandCreate, BrandList, BrandRead, BrandUpdate,
    MemberCreate, MemberList, MemberRead, MemberUpdate,
    MotorcycleCreate, MotorcycleList, MotorcycleRead, MotorcycleUpdate,
    RoleCreate, RoleList, RoleRead, RoleUpdate,
    UserCreate, UserList, UserRead, UserUpdate)
from core.database import DBSession as Session



router = APIRouter()



# Role endpoints

@router.get("/roles", response_model=list[RoleList])
def list_roles(session:Session, skip:int=0, limit:int=10) -> list[Role]:
    """List roles."""

    return crud.list_roles(session, skip, limit)



@router.post("/roles", response_model=RoleRead, status_code=201)
def create_role(session:Session, data:RoleCreate) -> Role:
    """Create a new role."""

    role = crud.get_role_by_name(session, data.name)
    if role:
        raise HTTPException(409, f"Role {data.name} already exists!")
    return crud.create_role(session, data)



@router.get("/roles/{role_id}", response_model=RoleRead)
def get_role(session:Session, role_id:int) -> Role:
    """Get a role by its ID."""

    role = crud.get_role_by_id(session, role_id)
    if not role:
        raise HTTPException(404, f"Role #{role_id} not found!")
    return role



@router.put("/roles/{role_id}", response_model=RoleRead)
def update_role(session:Session, role_id:int, data:RoleUpdate) -> Role:
    """Update a role."""

    role = crud.update_role(session, role_id, data)
    if not role:
        raise HTTPException(404, f"Role #{role_id} not found!")
    return role



@router.delete("/roles/{role_id}", status_code=204)
def delete_role(
    session:Session, role_id:int, hard:bool=False
) -> None:
    """Delete a role by its ID."""

    role = crud.get_role_by_id(session, role_id)
    if not role:
        raise HTTPException(404, f"Role #{role_id} not found!")
    crud.delete_role(session, role_id, hard)



# Role relationship endpoints

@router.get("/roles/{role_id}/users", response_model=list[UserList])
def list_role_users(session:Session, role_id:int):
    """Get the users with a role."""

    role = crud.get_role_by_id(session, role_id)
    if not role:
        raise HTTPException(404, f"Role #{role_id} not found!")
    return role.users



# Motorcycle endpoints

@router.get("/motorcycles", response_model=list[MotorcycleList])
def list_motorcycles(
    session:Session,
    skip:int=0,
    limit:int=10,
    brand_id:int|None=None,
    member_id:int|None=None
) -> list[Motorcycle]:
    """List motorcycles."""

    return crud.list_motorcycles(session, skip, limit, brand_id, member_id)



@router.post("/motorcycles", response_model=MotorcycleRead, status_code=201)
def create_motorcycle(session:Session, data:MotorcycleCreate) -> Motorcycle:
    """Create a new motorcycle."""

    motorcycle = crud.get_motorcycle_by_license_plate(
        session, data.license_plate
    )
    if motorcycle:
        raise HTTPException(
            409, f"Motorcycle {data.license_plate} already exists!"
        )
    return crud.create_motorcycle(session, data)



@router.get("/motorcycles/{motorcycle_id}", response_model=MotorcycleRead)
def get_motorcycle(session:Session, motorcycle_id:int) -> Motorcycle:
    """Get a motorcycle by its ID."""

    motorcycle = crud.get_motorcycle_by_id(session, motorcycle_id)
    if not motorcycle:
        raise HTTPException(404, f"Motorcycle #{motorcycle_id} not found!")
    return motorcycle



@router.put("/motorcycles/{motorcycle_id}", response_model=MotorcycleRead)
def update_motorcycle(
    session:Session, motorcycle_id:int, data:MotorcycleUpdate
) -> Motorcycle:
    """Update a motorcycle."""

    motorcycle = crud.update_motorcycle(session, motorcycle_id, data)
    if not motorcycle:
        raise HTTPException(404, f"Motorcycle #{motorcycle_id} not found!")
    return motorcycle



@router.delete("/motorcycles/{motorcycle_id}", status_code=204)
def delete_motorcycle(
    session:Session, motorcycle_id:int, hard:bool=False
) -> None:
    """Delete a motorcycle by its ID."""

    motorcycle = crud.get_motorcycle_by_id(session, motorcycle_id)
    if not motorcycle:
        raise HTTPException(404, f"Motorcycle #{motorcycle_id} not found!")
    crud.delete_motorcycle(session, motorcycle_id, hard)



# Motorcycle relationship endpoints

@router.get("/motorcycles/{motorcycle_id}/brand", response_model=BrandRead)
def list_motorcycle_brand(session:Session, motorcycle_id:int):
    """Get the brand of a motorcycle."""

    motorcycle = crud.get_motorcycle_by_id(session, motorcycle_id)
    if not motorcycle:
        raise HTTPException(404, f"Motorcycle #{motorcycle_id} not found!")
    return motorcycle.brand



@router.get("/motorcycles/{motorcycle_id}/owner", response_model=MemberRead)
def list_motorcycle_owner(session:Session, motorcycle_id:int):
    """Get the owner of a motorcycle."""

    motorcycle = crud.get_motorcycle_by_id(session, motorcycle_id)
    if not motorcycle:
        raise HTTPException(404, f"Motorcycle #{motorcycle_id} not found!")
    return motorcycle.member



# Brand endpoints

@router.get("/brands", response_model=list[BrandList])
def list_brands(session:Session, skip:int=0, limit:int=10) -> list[Brand]:
    """List brands."""

    return crud.list_brands(session, skip, limit)



@router.post("/brands", response_model=BrandRead, status_code=201)
def create_brand(session:Session, data:BrandCreate) -> Brand:
    """Create a new brand."""

    brand = crud.get_brand_by_name(session, data.name)
    if brand:
        raise HTTPException(409, f"Brand {data.name} already exists!")
    return crud.create_brand(session, data)



@router.get("/brands/{brand_id}", response_model=BrandRead)
def get_brand(session:Session, brand_id:int) -> Brand:
    """Get a brand by its ID."""

    brand = crud.get_brand_by_id(session, brand_id)
    if not brand:
        raise HTTPException(404, f"Brand #{brand_id} not found!")
    return brand



@router.put("/brands/{brand_id}", response_model=BrandRead)
def update_brand(session:Session, brand_id:int, data:BrandUpdate) -> Brand:
    """Update a brand."""

    brand = crud.update_brand(session, brand_id, data)
    if not brand:
        raise HTTPException(404, f"Brand #{brand_id} not found!")
    return brand



@router.delete("/brands/{brand_id}", status_code=204)
def delete_brand(session:Session, brand_id:int, hard:bool=False) -> None:
    """Delete a brand by its ID."""

    brand = crud.get_brand_by_id(session, brand_id)
    if not brand:
        raise HTTPException(404, f"Brand #{brand_id} not found!")
    crud.delete_brand(session, brand_id, hard)



# Brand relationship endpoints

@router.get(
    "/brands/{brand_id}/motorcycles", response_model=list[MotorcycleList]
)
def list_brand_motorcycles(session:Session, brand_id:int):
    """Get the motorcycles of a brand."""

    brand = crud.get_brand_by_id(session, brand_id)
    if not brand:
        raise HTTPException(404, f"Brand #{brand_id} not found!")
    return brand.motorcycles



# User endpoints
