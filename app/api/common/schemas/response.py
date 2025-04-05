import uuid

from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    message: str = Field(..., description="Message response")


class PostResponse(BaseModel):
    id: uuid.UUID = Field(
        ...,
        description='Id of the created resource',
        examples=['112d3e8b-a401-4868-a902-c0ac0736855c'],
    )
