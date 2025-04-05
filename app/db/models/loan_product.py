import uuid
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class LoanProductType(str, Enum):
    PERSONAL_LOAN = 'PersonalLoan'
    HOME_MORTGAGE = 'HomeMortgage'
    CREDIT_CARD = 'CreditCard'


class LoanProductPut(SQLModel):
    name: Optional[str] = Field(None)
    rate: Optional[float] = Field(None)


class LoanProductsPost(LoanProductPut):
    type: LoanProductType
    name: str
    rate: float


class LoanProduct(LoanProductsPost, table=True):
    __tablename__ = "loan_product"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True)
