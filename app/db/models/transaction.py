import uuid
from enum import Enum
from datetime import datetime
from typing import Optional

from pydantic import model_validator
from sqlmodel import Field, SQLModel


class TransactionType(str, Enum):
    WITHDRAW = "Withdraw"
    TRANSFER = "Transfer"
    DEPOSIT = "Deposit"


class TransactionsPost(SQLModel):
    amount: float
    description: str
    type: TransactionType
    fee: Optional[float] = Field(0.00)
    source_account_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="bank_account.id",
        index=True,
        alias="sourceAccountId",
        schema_extra=dict(
            validation_alias="sourceAccountId",
            serialization_alias="sourceAccountId"))
    destination_account_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="bank_account.id",
        index=True,
        alias="destinationAccountId",
        schema_extra=dict(
            validation_alias="destinationAccountId",
            serialization_alias="destinationAccountId"))

    @model_validator(mode="after")
    def check_transaction_type_validity(self):
        transaction_type: TransactionType = self.type
        source_account_id: str = self.source_account_id
        destination_account_id: str = self.destination_account_id

        if self.amount <= 0:
            raise ValueError('A transaction needs a positive amount.')

        if transaction_type is TransactionType.DEPOSIT and not destination_account_id:
            raise ValueError(f"A {transaction_type.value} needs a destination account.")
        if transaction_type is TransactionType.WITHDRAW and not source_account_id:
            raise ValueError(f"A {transaction_type.value} needs a source account.")
        if transaction_type is TransactionType.TRANSFER and (
                not source_account_id or not destination_account_id):
            raise ValueError(f"A {transaction_type.value} needs both source and destination accounts.")

        return self


class Transaction(TransactionsPost, table=True):
    __tablename__ = "transaction"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        alias="createdAt",
        schema_extra=dict(
            validation_alias="createdAt",
            serialization_alias="createdAt"))
