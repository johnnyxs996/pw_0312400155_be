from fastapi import APIRouter, Depends
from typing import Annotated

from app.api.common.schemas.response import (
    MessageResponse)
from app.core.jwt import get_current_active_user
from app.db import SessionDep
from app.db.models import (
    CredentialsPost, Token, UserProfile)
from app.services import (
    auth as auth_service)

router = APIRouter()

@router.post(
    "/login",
    responses={
        200: {
            "model": Token,
            "description": "Successful login"
        },
        400: {
            "model": MessageResponse,
            "description": "Invalid credentials"
        },
    },
    tags=["Auth"],
    summary="Authenticate user",
    response_model_by_alias=True,
)
async def login_post(
    login_post: CredentialsPost,
    session: SessionDep
) -> Token:
    return await auth_service.login_post(
        login_post, session)


@router.post(
    "/refresh",
    responses={
        200: {
            "model": Token,
            "description": "Successful token refresh"
        },
        400: {
            "model": MessageResponse,
            "description": "Invalid credentials"
        },
    },
    tags=["Auth"],
    summary="Refresh auth token",
)
async def refresh_token(refresh_token: str):
    return await auth_service.refresh_token(refresh_token)


@router.post(
    "/logout",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Logout message"
        },
    },
    tags=["Auth"],
    summary="Perform logout",
    response_model_by_alias=True,
)
async def logout_post(
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> MessageResponse:
    return await auth_service.logout_post()
