import random
import string
import uuid
from typing import Optional

from sqlmodel import Field, SQLModel


def _generate_random_swift_code() -> str:
    length = random.randint(8, 16)
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))


class BankPut(SQLModel):
    name: str = Field(..., index=True)


class BanksPost(BankPut):
    address: str
    phone: str


class Bank(BanksPost, table=True):
    __tablename__ = "bank"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True)
    swift_code: Optional[str] = Field(
        default_factory=_generate_random_swift_code,
        unique=True, min_length=8, max_length=16,
        alias="swiftCode",
        schema_extra=dict(
            validation_alias="swiftCode",
            serialization_alias="swiftCode"))
