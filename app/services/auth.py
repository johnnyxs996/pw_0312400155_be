import logging
from datetime import datetime, timedelta

from sqlmodel import select

from app.api.common.errors import InvalidCredentialsError
from app.api.common.schemas.response import (
    MessageResponse)
from app.core.jwt import authenticate_user, create_token, decode_token
from app.db import SessionDep
from app.db.models import (
    CredentialsPost, Token, UserProfile)

_log = logging.getLogger(__name__)


async def login_post(
    login_post: CredentialsPost,
    session: SessionDep
) -> Token:
    user_profile_query = select(UserProfile) \
        .where(UserProfile.email == login_post.email)
    user_profile = session.exec(
        user_profile_query).first()
    
    if not user_profile:
        raise InvalidCredentialsError()
    
    if not authenticate_user(user_profile, login_post):
        raise InvalidCredentialsError()
    
    user_profile.sqlmodel_update(
        dict(last_login=datetime.utcnow()))
    session.add(user_profile)
    session.commit()
    session.refresh(user_profile)
    return create_token(user_profile_id=str(user_profile.id))


async def refresh_token(refresh_token: str) -> Token:
    payload = decode_token(refresh_token)
    user_profile_id: str = payload.get("sub")
    if user_profile_id is None:
        raise InvalidCredentialsError()

    return create_token(user_profile_id=str(user_profile_id))


async def logout_post() -> MessageResponse:
    return MessageResponse(message="Logged out successfully")
