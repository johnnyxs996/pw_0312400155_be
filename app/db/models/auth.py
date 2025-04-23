from sqlmodel import Field, SQLModel, UniqueConstraint


class CredentialsPut(SQLModel):
    email: str = Field(..., unique=True, index=True)


class CredentialsPost(CredentialsPut):
    password: str = Field(..., exclude=True)

    __table_args__ = (UniqueConstraint("email", "password"),)


class RefreshCredentials(SQLModel):
    refresh_token: str
