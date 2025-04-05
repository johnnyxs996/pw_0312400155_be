import uuid

from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(SQLModel):
    id: uuid.UUID