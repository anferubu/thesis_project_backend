from datetime import date

from sqlalchemy import func
from sqlmodel import select, Session

from api.crud.utils import apply_filters, apply_sorting
from api.models.users import Brand, Profile, Motorcycle, Role, User
from api.schemas.users import (
    RoleCreate, RoleUpdate, BrandCreate, BrandUpdate, MotorcycleCreate,
    MotorcycleUpdate, UserCreate, UserUpdate)
from api.utils.security.hashing import get_password_hash



# Role model CRUD

def create_role(session:Session, data:RoleCreate) -> Role:
    """Create a role."""

    new_role = Role.model_validate(data)
    session.add(new_role)
    session.commit()
    session.refresh(new_role)
    return new_role



def get_role_by_id(session:Session, role_id:int) -> Role|None:
    """Get a role by its ID."""

    role = session.get(Role, role_id)
    return role if role and not role.deleted else None



def get_role_by_name(session:Session, name:str) -> Role|None:
    """Get a role by its name."""

    query = select(Role).where(
        func.lower(Role.name) == name.lower(), Role.deleted == False
    )
    return session.exec(query).first()



def list_roles(
    session:Session,
    skip:int|None=None,
    limit:int|None=None,
    sort: dict[str, str]|None = None,
    filter: dict[str, any]|None = None
) -> list[Role]:
    """List roles."""

    query = select(Role).where(Role.deleted == False)
    if filter:
        query = apply_filters(query, Role, filter)
    if sort:
        query = apply_sorting(query, Role, sort)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return session.exec(query).all()



def update_role(session:Session, role_id:int, data:RoleUpdate) -> Role|None:
    """Update a role."""

    role = session.get(Role, role_id)
    if role:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(role, field, value)
        session.commit()
        session.refresh(role)
    return role



def delete_role(session:Session, role_id:int, hard:bool=False) -> None:
    """Delete a role."""

    role = session.get(Role, role_id)
    if role:
        if hard:
            session.delete(role)
            session.commit()
        else:
            role.deleted = True
            session.commit()
            session.refresh(role)



# Motorcycle model CRUD

def create_motorcycle(session:Session, data:MotorcycleCreate) -> Motorcycle:
    """Create a motorcycle."""

    new_motorcycle = Motorcycle.model_validate(data)
    session.add(new_motorcycle)
    session.commit()
    session.refresh(new_motorcycle)
    return new_motorcycle



def get_motorcycle_by_id(
    session:Session, motorcycle_id:int
) -> Motorcycle|None:
    """Get a motorcycle by its ID."""

    motorcycle = session.get(Motorcycle, motorcycle_id)
    return motorcycle if motorcycle and not motorcycle.deleted else None



def get_motorcycle_by_license_plate(
        session:Session, license_plate:str) -> Motorcycle|None:
    """Get a motorcycle by its license plate."""

    query = select(Motorcycle).where(
        func.lower(Motorcycle.license_plate) == license_plate.lower(),
        Motorcycle.deleted == False
    )
    return session.exec(query).first()



def list_motorcycles(
    session:Session,
    skip:int|None=None,
    limit:int|None=None,
    sort: dict[str, str]|None = None,
    filter: dict[str, any]|None = None
) -> list[Motorcycle]:
    """List motorcycles."""

    query = select(Motorcycle).where(Motorcycle.deleted == False)
    if filter:
        query = apply_filters(query, Motorcycle, filter)
    if sort:
        query = apply_sorting(query, Motorcycle, sort)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return session.exec(query).all()



def update_motorcycle(
        session:Session, motorcycle_id:int, data:MotorcycleUpdate
) -> Motorcycle|None:
    """Update a motorcycle."""

    motorcycle = session.get(Motorcycle, motorcycle_id)
    if motorcycle:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(motorcycle, field, value)
        session.commit()
        session.refresh(motorcycle)
    return motorcycle



def delete_motorcycle(
        session:Session, motorcycle_id:int, hard:bool=False
) -> None:
    """Delete a motorcycle."""

    motorcycle = session.get(Motorcycle, motorcycle_id)
    if motorcycle:
        if hard:
            session.delete(motorcycle)
            session.commit()
        else:
            motorcycle.deleted = True
            session.commit()
            session.refresh(motorcycle)



# Brand model CRUD

def create_brand(session:Session, data:BrandCreate) -> Brand:
    """Create a brand."""

    new_brand = Brand.model_validate(data)
    session.add(new_brand)
    session.commit()
    session.refresh(new_brand)
    return new_brand



def get_brand_by_id(session:Session, brand_id:int) -> Brand|None:
    """Get a brand by its ID."""

    brand = session.get(Brand, brand_id)
    return brand if brand and not brand.deleted else None



def get_brand_by_name(session:Session, name:str) -> Brand|None:
    """Get a brand by its name."""

    query = select(Brand).where(
        func.lower(Brand.name) == name.lower(), Brand.deleted == False
    )
    return session.exec(query).first()



def list_brands(
    session:Session,
    skip:int|None=None,
    limit:int|None=None,
    sort: dict[str, str]|None = None,
    filter: dict[str, any]|None = None
) -> list[Brand]:
    """List brands."""

    query = select(Brand).where(Brand.deleted == False)
    if filter:
        query = apply_filters(query, Brand, filter)
    if sort:
        query = apply_sorting(query, Brand, sort)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return session.exec(query).all()



def update_brand(
        session:Session, brand_id:int, data:BrandUpdate
) -> Brand|None:
    """Update a brand."""

    brand = session.get(Brand, brand_id)
    if brand:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(brand, field, value)
        session.commit()
        session.refresh(brand)
    return brand



def delete_brand(
        session:Session, brand_id:int, hard:bool=False
) -> None:
    """Delete a brand."""

    brand = session.get(Brand, brand_id)
    if brand:
        if hard:
            session.delete(brand)
            session.commit()
        else:
            brand.deleted = True
            session.commit()
            session.refresh(brand)



# User model CRUD

def create_user(session:Session, data:UserCreate) -> User:
    """Create a user (and its profile)."""

    user_data = data.model_dump(exclude={"profile"})
    profile_data = data.profile.model_dump()
    user = User.model_validate(
        user_data,
        update={"password": get_password_hash(data.password)}
    )
    profile = Profile(**profile_data, user=user)
    session.add_all([user, profile])
    session.commit()
    session.refresh(user)
    return user



def get_user_by_id(session:Session, user_id:int) -> User|None:
    """Get a user by its ID."""

    user = session.get(User, user_id)
    return user if user and not user.deleted else None



def get_profile_by_id(session:Session, profile_id:int) -> Profile|None:
    """Get a profile by its ID."""

    profile = session.get(Profile, profile_id)
    return profile if profile and not profile.deleted else None



def get_user_by_email(session:Session, email:str) -> User|None:
    """Get a user by its email."""

    query = select(User).where(User.email == email, User.deleted == False)
    return session.exec(query).first()



def list_users(
    session:Session,
    skip:int|None=None,
    limit:int|None=None,
    sort: dict[str, str]|None = None,
    filter: dict[str, any]|None = None
) -> list[User]:
    """List users."""

    query = select(User).where(User.deleted == False)
    if filter:
        query = apply_filters(query, User, filter)
    if sort:
        query = apply_sorting(query, User, sort)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return session.exec(query).all()



def update_user(session:Session, user_id:int, data:UserUpdate) -> User|None:
    """Update a user (and its profile)."""

    user = session.get(User, user_id)
    user_data = data.model_dump(exclude_unset=True, exclude={"profile"})
    for key, value in user_data.items():
        setattr(user, key, value)
    if data.profile:
        profile_data = data.profile.model_dump(exclude_unset=True)
        for key, value in profile_data.items():
            setattr(user.profile, key, value)
    session.commit()
    session.refresh(user)
    return user



def delete_user(session:Session, user_id:int, hard:bool=False) -> None:
    """Delete a user (and its profile)."""

    user = session.get(User, user_id)
    if user:
        if hard:
            if user.profile:
                session.delete(user.profile)
            session.delete(user)
            session.commit()
        else:
            user.deleted = True
            user.profile.deleted = True
            session.commit()
            session.refresh(user)



def change_password(session:Session, user_id:int, new_password:str) -> User:
    user = session.get(User, user_id)
    hashed_password = get_password_hash(new_password)
    user.password = hashed_password
    session.add(user)
    session.commit()
    session.refresh(user)
    return user



def list_users_birthday_is_today(session:Session) -> list[User]:
    """Get users whose birthday is today."""

    today = date.today()
    query = select(User).where(
        User.deleted == False,
        User.profile.has(Profile.birthdate == today)
    )
    return session.exec(query).all()



def list_users_by_birthdate(session:Session, date:date) -> list[User]:
    """List users by its birthdate."""

    query = select(User).where(
        User.deleted == False,
        User.profile.has(Profile.birthdate == date)
    )
    return session.exec(query).all()



def list_users_by_birthdate_range(
        session:Session, start_date:date, end_date:date
) -> list[User]:
    """List users by a birthdate range."""

    query = select(User).where(
        User.deleted == False,
        User.profile.has(Profile.birthdate >= start_date),
        User.profile.has(Profile.birthdate <= end_date)
    )
    return session.exec(query).all()
