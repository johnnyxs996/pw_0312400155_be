import uuid
from enum import Enum
from datetime import datetime
from typing import Optional

from pydantic import field_validator
from sqlmodel import Column, Field, SQLModel
from sqlmodel import Enum as SQLEnum

from app.utils.dates import string_to_date


class InvestmentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


class InvestmentAction(str, Enum):
    ACTIVATE = 'activate'
    CLOSE = 'close'


class InvestmentsPost(SQLModel):
    amount: float
    start_date: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        alias="startDate",
        schema_extra=dict(
            validation_alias="startDate",
            serialization_alias="startDate"))
    end_date: datetime = Field(
        ...,
        alias="endDate",
        schema_extra=dict(
            validation_alias="endDate",
            serialization_alias="endDate"))
    investment_product_id: uuid.UUID = Field(
        ...,
        foreign_key="investment_product.id",
        alias="investmentProductId",
        schema_extra=dict(
            validation_alias="investmentProductId",
            serialization_alias="investmentProductId"))
    bank_account_id: uuid.UUID = Field(
        ...,
        foreign_key="bank_account.id",
        index=True,
        alias="bankAccountId",
        schema_extra=dict(
            validation_alias="bankAccountId",
            serialization_alias="bankAccountId"))
    
    @field_validator("amount", mode="before")
    def round_decimals(cls, value):
        if isinstance(value, float):
            return round(value, 2)
        return value

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            return string_to_date(value)
        return value


class Investment(InvestmentsPost, table=True):
    __tablename__ = "investment"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True)
    status_id: Optional[InvestmentStatus] = Field(
        sa_column=Column(SQLEnum(InvestmentStatus)),
        default=InvestmentStatus.ACTIVE,
        alias="status",
        schema_extra=dict(
            validation_alias="status",
            serialization_alias="status"))


class InvestmentActionPost(SQLModel):
    action: InvestmentAction
