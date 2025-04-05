import uuid
from datetime import datetime
from typing import Optional

from pydantic import field_validator
from sqlmodel import Field, SQLModel

from app.utils.dates import string_to_date


class UsersPost(SQLModel):
    name: str = Field(..., index=True)
    surname: str = Field(..., index=True)
    tax_identification_number: str = Field(
        ..., unique=True, min_length=16, max_length=16,
        alias="taxIdentificationNumber",
        schema_extra=dict(
            validation_alias="taxIdentificationNumber",
            serialization_alias="taxIdentificationNumber"))
    birth_date: Optional[datetime] = Field(
        None,
        alias="birthDate",
        schema_extra=dict(
            validation_alias="birthDate",
            serialization_alias="birthDate"))
    birth_country: Optional[str] = Field(
        None, min_length=3, max_length=3,
        alias="birthCountry",
        schema_extra=dict(
            validation_alias="birthCountry",
            serialization_alias="birthCountry"))
    birth_state: Optional[str] = Field(
        None, min_length=2, max_length=2,
        alias="birthState",
        schema_extra=dict(
            validation_alias="birthState",
            serialization_alias="birthState"))
    birth_city: Optional[str] = Field(
        None,
        alias="birthCity",
        schema_extra=dict(
            validation_alias="birthCity",
            serialization_alias="birthCity"))

    @field_validator("birth_date", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            return string_to_date(value)
        return value


class User(UsersPost, table=True):
    __tablename__ = "user"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
