import uuid
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class InvestmentProductType(str, Enum):
    ACTION = 'Action'
    ETF = 'ETF'
    FUND = 'Fund'
    BOND = 'Bond'
    CRYPTO = 'Crypto'
    RAW_MATERIALS = 'RawMaterials'


class InvestmentProductPut(SQLModel):
    name: Optional[str] = Field(None)
    rate: Optional[float] = Field(None)


class InvestmentProductsPost(InvestmentProductPut):
    type: InvestmentProductType
    name: str
    rate: float


class InvestmentProduct(InvestmentProductsPost, table=True):
    __tablename__ = "investment_product"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True)
