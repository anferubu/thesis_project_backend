from datetime import date, datetime
import re
from typing import Any, Annotated

from pydantic import EmailStr, FilePath, field_validator, model_validator
from sqlmodel import Field, SQLModel

from api.models.utils.enums import UserStatus, DocumentType, GenderType, RHType
from api.schemas import utils



# Token schemas

class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequest(SQLModel):
    refresh_token: str



# User-Profile schemas

class ProfileBase(SQLModel):
    telephone: str|None = None

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        values = utils.remove_whitespaces(values)
        values = utils.check_telephone(values, "telephone")
        return values


class ProfileCreate(ProfileBase):
    first_name: Annotated[str, Field(min_length=3, max_length=25)]
    last_name: Annotated[str, Field(min_length=3, max_length=25)]
    nickname: Annotated[str|None, Field(min_length=3, max_length=25)] = None
    telephone: str|None = None
    document_type: DocumentType
    document_number: str
    rh: RHType
    birthdate: date
    genre: GenderType
    photo: FilePath|None = None
    team_id: int

    @field_validator('birthdate')
    def validate_birthdate(cls, value:str) -> str:
        """Validates the field 'birthdate' in the creation schema."""

        today = datetime.today().date()
        min_age = 18
        min_date = today.replace(year=today.year - min_age)
        if value > today:
            raise ValueError("Birthdate cannot be in the future.")
        if value > min_date:
            raise ValueError(f"User must be at least {min_age} years old.")
        return value


class ProfileUpdate(ProfileBase):
    first_name: Annotated[str|None, Field(min_length=3, max_length=25)] = None
    last_name: Annotated[str|None, Field(min_length=3, max_length=25)] = None
    nickname: Annotated[str|None, Field(min_length=3, max_length=25)] = None
    telephone: str|None = None
    photo: FilePath|None = None
    team_id: int|None = None


class ProfileRead(SQLModel):
    first_name: str
    last_name: str
    nickname: str|None = None
    telephone: str|None = None
    document_type: DocumentType
    document_number: str
    rh: RHType
    birthdate: date
    genre: GenderType
    photo: FilePath|None = None
    team_id: int


class UserCreate(SQLModel):
    email: EmailStr
    password: str
    role_id: int|None = None
    status: UserStatus|None = None
    profile: ProfileCreate

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        """Validates the creation/update schema data."""

        # validate password
        values = utils.check_password(values, "password")
        return values


class UserUpdate(SQLModel):
    role_id: int|None = None
    status: UserStatus|None = None
    profile: ProfileUpdate|None = None


class UserRead(SQLModel):
    id: int
    email: EmailStr
    role_id: int
    status: UserStatus
    profile: ProfileRead
    created_at: datetime
    updated_at: datetime


class UserList(SQLModel):
    id: int
    email: EmailStr



# Password schemas

class PasswordChange(SQLModel):
    old_password: str
    new_password: str

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        values = utils.check_password(values, "new_password")
        return values


class PasswordReset(SQLModel):
    new_password: str

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        values = utils.check_password(values, "new_password")
        return values


class RequestPasswordReset(SQLModel):
    email: EmailStr



# Role schemas

class RoleCreate(SQLModel):
    name: Annotated[str, Field(min_length=3, max_length=20)]
    description: Annotated[str|None, Field(max_length=50)] = None

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        values = utils.remove_whitespaces(values)
        return values


class RoleUpdate(RoleCreate):
    name: Annotated[str|None, Field(min_length=3, max_length=20)] = None
    description: Annotated[str|None, Field(max_length=50)] = None


class RoleRead(SQLModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class RoleList(SQLModel):
    id: int
    name: str



# Motorcycle schemas

class MotorcycleBase(SQLModel):

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        values = utils.remove_whitespaces(values)
        return values


class MotorcycleCreate(MotorcycleBase):
    model: Annotated[str, Field(min_length=3, max_length=25)]
    license_plate: str
    photo: FilePath|None = None
    brand_id: int
    owner_id: int

    @field_validator('license_plate')
    def validate_license_plate(cls, value:str) -> str:
        """Validates the field 'license_plate' in the creation schema."""

        if not re.match(r'^[A-Z]{3}\d{3}$', value):
            raise ValueError("license_plate must be in the format 'ABC123'.")
        return value


class MotorcycleUpdate(MotorcycleBase):
    photo: FilePath|None = None
    owner_id: int|None = None


class MotorcycleRead(SQLModel):
    id: int
    model: str
    license_plate: str
    photo: FilePath|None = None
    brand_id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime


class MotorcycleList(SQLModel):
    id: int
    model: str
    license_plate: str
    brand_id: int
    owner_id: int



# Brand schemas

class BrandCreate(SQLModel):
    name: Annotated[str, Field(min_length=3, max_length=25)]

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        values = utils.remove_whitespaces(values)
        return values


class BrandUpdate(BrandCreate):
    name: Annotated[str|None, Field(min_length=3, max_length=25)] = None


class BrandRead(SQLModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class BrandList(SQLModel):
    id: int
    name: str
