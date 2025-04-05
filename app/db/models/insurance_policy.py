import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import field_validator
from sqlmodel import Column, Field, SQLModel
from sqlmodel import Enum as SQLEnum

from app.utils.dates import string_to_date


class InsurancePolicyStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


class InsurancePolicyAction(str, Enum):
    SUSPEND = 'suspend'
    REACTIVATE = 'reactivate'


class InsurancePoliciesPost(SQLModel):
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
    insurance_policy_product_id: uuid.UUID = Field(
        default=None,
        foreign_key="insurance_policy_product.id",
        alias="insurancePolicyProductId",
        schema_extra=dict(
            validation_alias="insurancePolicyProductId",
            serialization_alias="insurancePolicyProductId"))
    bank_account_id: uuid.UUID = Field(
        default=None,
        foreign_key="bank_account.id",
        index=True,
        alias="bankAccountId",
        schema_extra=dict(
            validation_alias="bankAccountId",
            serialization_alias="bankAccountId"))

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            return string_to_date(value)
        return value


class InsurancePolicy(InsurancePoliciesPost, table=True):
    __tablename__ = "insurance_policy"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True)
    status_id: Optional[InsurancePolicyStatus] = Field(
        sa_column=Column(SQLEnum(InsurancePolicyStatus)),
        default=InsurancePolicyStatus.ACTIVE,
        alias="status",
        schema_extra=dict(
            validation_alias="status",
            serialization_alias="status"))


class InsurancePolicyActionPost(SQLModel):
    action: InsurancePolicyAction
