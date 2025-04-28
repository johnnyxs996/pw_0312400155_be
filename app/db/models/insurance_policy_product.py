import uuid
from enum import Enum
from typing import Optional

from pydantic import field_validator
from sqlmodel import Field, SQLModel


class InsurancePolicyProductType(str, Enum):
    CAR = 'Car'
    LIFE = 'Life'
    HOME = 'Home'


class InsurancePolicyProductPut(SQLModel):
    name: Optional[str] = Field(None)
    annual_premium: Optional[float] = Field(
        None,
        alias="annualPremium",
        schema_extra=dict(
            validation_alias="annualPremium",
            serialization_alias="annualPremium"))
    coverage_cap: Optional[float] = Field(
        None,
        alias="coverageCap",
        schema_extra=dict(
            validation_alias="coverageCap",
            serialization_alias="coverageCap"))
    
    @field_validator("annual_premium", "coverage_cap", mode="before")
    def round_decimals(cls, value):
        if isinstance(value, float):
            return round(value, 2)
        return value


class InsurancePolicyProductsPost(InsurancePolicyProductPut):
    type: InsurancePolicyProductType
    name: str
    annual_premium: float = Field(
        ...,
        alias="annualPremium",
        schema_extra=dict(
            validation_alias="annualPremium",
            serialization_alias="annualPremium"))
    coverage_cap: float = Field(
        ...,
        alias="coverageCap",
        schema_extra=dict(
            validation_alias="coverageCap",
            serialization_alias="coverageCap"))


class InsurancePolicyProduct(InsurancePolicyProductsPost, table=True):
    __tablename__ = "insurance_policy_product"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True)
