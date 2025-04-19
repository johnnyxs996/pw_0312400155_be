import random
import string
import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


def _generate_random_iban_code() -> str:
    length = random.randint(10, 34)
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))


def _generate_random_account_number(
    account_number_length: Optional[int] = 10
) -> str:
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=account_number_length))


class BankAccountPut(SQLModel):
    bank_id: uuid.UUID = Field(
        default=None,
        foreign_key="bank.id",
        index=True,
        alias="bankId",
        schema_extra=dict(
            validation_alias="bankId",
            serialization_alias="bankId")
    )


class BankAccountsPost(BankAccountPut):
    currency: str = Field(
        ...,
        min_length=3,
        max_length=3)


class BankAccount(BankAccountsPost, table=True):
    __tablename__ = "bank_account"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True)
    iban_code: str = Field(
        default_factory=_generate_random_iban_code,
        unique=True, min_length=10, max_length=34,
        alias="ibanCode",
        schema_extra=dict(
            validation_alias="ibanCode",
            serialization_alias="ibanCode"))
    account_number: str = Field(
        default_factory=_generate_random_account_number,
        unique=True, min_length=10, max_length=10,
        alias="accountNumber",
        schema_extra=dict(
            validation_alias="accountNumber",
            serialization_alias="accountNumber"))
    balance: Optional[float] = Field(
        default=0.00)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        alias="createdAt",
        schema_extra=dict(
            validation_alias="createdAt",
            serialization_alias="createdAt"))
    user_profile_id: uuid.UUID = Field(
        default=None, foreign_key="user_profile.id",
        index=True,
        alias="userProfileId",
        schema_extra=dict(
            validation_alias="userProfileId",
            serialization_alias="userProfileId"))
