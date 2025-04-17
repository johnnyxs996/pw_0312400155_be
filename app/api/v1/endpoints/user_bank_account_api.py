from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from app.api.common.schemas.response import (
    MessageResponse, PostResponse)
from app.core.jwt import get_current_active_user
from app.db import SessionDep
from app.db.models import (
    BankAccount, BankAccountsPost, UserProfile)
from app.services import (
    user_bank_account as user_bank_account_service)

router = APIRouter()

@router.get(
    "/userProfiles/{user_profile_id}/bankAccounts",
    responses={
        200: {
            "model": Page[BankAccount],
            "description": "A list of user bank accounts"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["User Bank Account"],
    summary="List all user bank accounts",
    response_model_by_alias=True,
)
async def user_profiles_id_bank_accounts_get(
    user_profile_id: str,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> Page[BankAccount]:
    return await user_bank_account_service.user_profiles_id_bank_accounts_get(
        user_profile_id, session)


@router.post(
    "/userProfiles/{user_profile_id}/bankAccounts",
    responses={
        201: {
            "model": PostResponse,
            "description": "Base resource creation response"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["User Bank Account"],
    summary="Create a bank account for the user",
    response_model_by_alias=True,
)
async def user_profiles_id_bank_accounts_post(
    user_profile_id: str,
    bank_accounts_post: BankAccountsPost,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> PostResponse:
    return await user_bank_account_service.user_profiles_id_bank_accounts_post(
        user_profile_id, bank_accounts_post, session)
