import uuid
from enum import Enum
from datetime import datetime
from typing import Optional

from pydantic import field_validator
from sqlmodel import Column, Field, SQLModel
from sqlmodel import Enum as SQLEnum

from app.utils.dates import string_to_date


class LoanStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


class LoansPost(SQLModel):
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
    loan_product_id: uuid.UUID = Field(
        ...,
        foreign_key="loan_product.id",
        alias="loanProductId",
        schema_extra=dict(
            validation_alias="loanProductId",
            serialization_alias="loanProductId"))
    bank_account_id: uuid.UUID = Field(
        ...,
        foreign_key="bank_account.id",
        index=True,
        alias="bankAccountId",
        schema_extra=dict(
            validation_alias="bankAccountId",
            serialization_alias="bankAccountId"))

    @field_validator("amount", mode="before")
    @classmethod
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


class Loan(LoansPost, table=True):
    __tablename__ = "loan"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True)
    status_id: Optional[LoanStatus] = Field(
        sa_column=Column(SQLEnum(LoanStatus)),
        default=LoanStatus.ACTIVE,
        alias="status",
        schema_extra=dict(
            validation_alias="status",
            serialization_alias="status"))
