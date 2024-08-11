from datetime import datetime

from pydantic import ConfigDict
from sqlmodel import SQLModel, Field



class Base(SQLModel):
    """Base model for the other tables in the database."""
    model_config = ConfigDict(
        strict=True,
        str_strip_whitespace=True,
    )

    id: int|None = Field(default=None, primary_key=True)
    deleted: bool = Field(default=False)
    deleted_at: datetime|None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now,
                                 sa_column_kwargs={"onupdate": datetime.now})
