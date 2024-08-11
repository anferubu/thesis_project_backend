from datetime import date, datetime
import re
from typing import Any, Annotated

from pydantic import model_validator
from sqlmodel import Field, SQLModel

from api.schemas import utils



# Agreement schemas

class AgreementBase(SQLModel):
    start_date: date
    end_date: date

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        values = utils.remove_whitespaces(values)
        values = utils.check_start_end_dates(values)
        return values


class AgreementCreate(AgreementBase):
    name: Annotated[str, Field(min_length=3, max_length=50)]
    description: Annotated[str|None, Field(max_length=2500)] = None
    start_date: date
    end_date: date
    active: bool = True
    company_id: int


class AgreementUpdate(AgreementBase):
    name: Annotated[str|None, Field(min_length=3, max_length=50)] = None
    description: Annotated[str|None, Field(max_length=2500)] = None
    start_date: date|None = None
    end_date: date|None = None
    active: bool|None = None


class AgreementRead(SQLModel):
    id: int
    name: str
    description: str|None = None
    start_date: date
    end_date: date
    active: bool = True
    company_id: int
    created_at: datetime
    updated_at: datetime


class AgreementList(SQLModel):
    id: int
    name: str
    start_date: date
    end_date: date
    active: bool



# Company schemas

class CompanyCreate(SQLModel):
    name: Annotated[str, Field(min_length=3, max_length=50)]
    contact_name: Annotated[str, Field(min_length=3, max_length=25)]
    contact_telephone: str
    contact_address: Annotated[str|None, Field(max_length=100)] = None
    location_id: int

    @model_validator(mode="before")
    def validate_schema(cls, values:Any) -> Any:
        values = utils.remove_whitespaces(values)
        values = utils.check_telephone(values, "contact_telephone")

        # remove whitespaces at beginning and end of a string.
        for key, value in values.items():
            if isinstance(value, str):
                values[key] = value.strip()
        # validate telephone
        telephone = values.get("contact_telephone")
        telephone = re.sub(r'[^\d]', '', telephone)
        values["contact_telephone"] = telephone
        if telephone and not re.match(r'^3\d{9}$', telephone):
            raise ValueError(
                "Phone number must be a valid mobile number, e.g., 3001234567."
            )
        return values


class CompanyUpdate(CompanyCreate):
    name: Annotated[str|None, Field(min_length=3, max_length=50)] = None
    contact_name: Annotated[str|None, Field(min_length=3, max_length=25)] = None
    contact_telephone: str|None = None
    contact_address: Annotated[str|None, Field(max_length=100)] = None
    location_id: int|None = None


class CompanyRead(SQLModel):
    id: int
    name: str
    contact_name: str
    contact_telephone: str
    contact_address: str|None = None
    location_id: int
    created_at: datetime
    updated_at: datetime


class CompanyList(SQLModel):
    id: int
    name: str
