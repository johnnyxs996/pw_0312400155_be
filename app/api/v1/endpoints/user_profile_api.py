from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from app.api.common.schemas.response import (
    MessageResponse, PostResponse)
from app.core.jwt import get_current_active_user
from app.db import SessionDep
from app.db.models import (
    CredentialsPut, UserProfile,
    UserProfilesPost, UserProfileWithUserData)
from app.services import (
    user_profile as user_profile_service)

router = APIRouter()

@router.get(
    "/userProfiles",
    responses={
        200: {
            "model": Page[UserProfile],
            "description": "A list of user profiles"
        },
    },
    tags=["User Profile"],
    summary="List all user profiles",
    response_model_by_alias=True,
)
async def user_profiles_get(
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> Page[UserProfile]:
    return await user_profile_service.user_profiles_get(
        session)


@router.delete(
    "/userProfiles/{id}",
    responses={
        204: {"description": "User profile deleted"},
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["User Profile"],
    summary="Delete a user profile",
    response_model_by_alias=True,
)
async def user_profiles_id_delete(
    id: str,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> None:
    return await user_profile_service.user_profiles_id_delete(
        id, session)


@router.get(
    "/userProfiles/{id}",
    responses={
        200: {
            "model": UserProfileWithUserData,
            "description": "User profile details"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["User Profile"],
    summary="Get a user profile",
    response_model_by_alias=True,
)
async def user_profiles_id_get(
    id: str,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> UserProfileWithUserData:
    return await user_profile_service.user_profiles_id_get(
        id, session)


@router.put(
    "/userProfiles/{id}",
    responses={
        200: {
            "model": UserProfileWithUserData,
            "description": "Updated user profile details"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["User Profile"],
    summary="Update a user profile",
    response_model_by_alias=True,
)
async def user_profiles_id_put(
    id: str,
    user_profile_put: CredentialsPut,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> UserProfileWithUserData:
    return await user_profile_service.user_profiles_id_put(
        id, user_profile_put, session)


@router.post(
    "/userProfiles",
    responses={
        201: {
            "model": PostResponse,
            "description": "Base resource creation response"
        },
    },
    tags=["User Profile"],
    summary="Create a user profile",
    response_model_by_alias=True,
)
async def user_profiles_post(
    user_profiles_post: UserProfilesPost,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> PostResponse:
    return await user_profile_service.user_profiles_post(
        user_profiles_post, session)
