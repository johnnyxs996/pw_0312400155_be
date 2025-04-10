from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.api.common.errors import InvalidCredentialsError
from app.core.config import settings
from app.db import SessionDep
from app.db.models import CredentialsPost, Token, TokenData, UserProfile
from app.services.user_profile import _get_full_user_profile_from_db
from app.utils.secrets import verify_password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(
    user_profile: UserProfile,
    credentials_post: CredentialsPost
) -> UserProfile:
    if not verify_password(
        credentials_post.password, user_profile.password
    ):
        return False
    return user_profile


async def get_current_user_profile(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep
) -> UserProfile:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        id = payload.get("sub")
        if id is None:
            raise InvalidCredentialsError()
        token_data = TokenData(id=id)
    except InvalidTokenError:
        raise InvalidCredentialsError()
    user_profile = await _get_full_user_profile_from_db(
        id=token_data.id, session=session)
    if user_profile is None:
        raise InvalidCredentialsError()
    return user_profile


async def get_current_active_user(
    current_user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
):
    return current_user_profile


def _create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    issued_at = datetime.now(timezone.utc)
    expire = issued_at + expires_delta
    duration = (expire - issued_at).total_seconds() * 1000

    to_encode.update({
        "iat": issued_at,
        "exp": expire,
        "dur": duration
    })
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_token(
    user_profile_id: str
) -> Token:
    access_token_expires = timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = access_token_expires + timedelta(minutes=5)
    access_token = _create_token(
        data={"sub": user_profile_id}, expires_delta=access_token_expires
    )
    refresh_token = _create_token(
        data={"sub": user_profile_id}, expires_delta=refresh_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="Bearer")


def decode_token(token: str):
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
