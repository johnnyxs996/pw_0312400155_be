from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from app.api.common.schemas.response import (
    MessageResponse)
from app.core.jwt import get_current_active_user
from app.db import SessionDep
from app.db.models import (
    BankAccount, BankAccountPut, UserProfile)
from app.services import (
    bank_account as bank_account_service)

router = APIRouter()

@router.get(
    "/bankAccounts",
    responses={
        200: {
            "model": Page[BankAccount],
            "description": "A list of bank accounts"
        },
    },
    tags=["Bank Account"],
    summary="List all bank accounts",
    response_model_by_alias=True,
)
async def bank_accounts_get(
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> Page[BankAccount]:
    return await bank_account_service.bank_accounts_get(
        session)


@router.delete(
    "/bankAccounts/{id}",
    responses={
        204: {
            "description": "Bank account deleted"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Bank Account"],
    summary="Delete a bank account",
    response_model_by_alias=True,
)
async def bank_accounts_id_delete(
    id: str, session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> None:
    return await bank_account_service.bank_accounts_id_delete(
        id, session)


@router.get(
    "/bankAccounts/{id}",
    responses={
        200: {
            "model": BankAccount,
            "description": "Bank account details"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Bank Account"],
    summary="Get a bank account",
    response_model_by_alias=True,
)
async def bank_accounts_id_get(
    id: str, session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> BankAccount:
    return await bank_account_service.bank_accounts_id_get(
        id, session)


@router.put(
    "/bankAccounts/{id}",
    responses={
        200: {
            "model": BankAccount,
            "description": "Bank account updated"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Bank Account"],
    summary="Update a bank account",
    response_model_by_alias=True,
)
async def bank_accounts_id_put(
    id: str, bank_account_put: BankAccountPut,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> BankAccount:
    return await bank_account_service.bank_accounts_id_put(
        id, bank_account_put, session)
