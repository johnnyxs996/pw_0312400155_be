import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from app.db.models import CredentialsPost, UsersPost


class UserProfilesPost(CredentialsPost, UsersPost):
    pass


class UserProfile(CredentialsPost, table=True):
    __tablename__ = "user_profile"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True)
    last_login: Optional[datetime] = Field(
        None,
        alias="lastLogin",
        schema_extra=dict(
            serialization_alias="lastLogin"))
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        alias="createdAt",
        schema_extra=dict(
            serialization_alias="createdAt"))
    user_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="user.id",
        index=True,
        alias="userId",
        schema_extra=dict(
            serialization_alias="userId"))


class UserProfileWithUserData(SQLModel):
    id: uuid.UUID
    email: str
    last_login: Optional[datetime] = Field(
        None,
        alias="lastLogin",
        schema_extra=dict(
            serialization_alias="lastLogin"))
    created_at: datetime = Field(
        ...,
        alias="createdAt",
        schema_extra=dict(
            serialization_alias="createdAt"))
    name: str
    surname: str
    tax_identification_number: str = Field(
        ...,
        alias="taxIdentificationNumber",
        schema_extra=dict(
            serialization_alias="taxIdentificationNumber"))
    birth_date: Optional[datetime] = Field(
        None,
        alias="birthDate",
        schema_extra=dict(
            serialization_alias="birthDate"))
    birth_country: Optional[str] = Field(
        None, min_length=3, max_length=3,
        alias="birthCountry",
        schema_extra=dict(
            serialization_alias="birthCountry"))
    birth_state: Optional[str] = Field(
        None,
        alias="birthState",
        schema_extra=dict(
            serialization_alias="birthState"))
    birth_city: Optional[str] = Field(
        None,
        alias="birthCity",
        schema_extra=dict(
            serialization_alias="birthCity"))