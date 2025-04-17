from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from app.api.common.schemas.response import (
    MessageResponse, PostResponse)
from app.core.jwt import get_current_active_user
from app.db import SessionDep
from app.db.models import (
    Bank, BanksPost, BankPut, UserProfile)
from app.services import (
    bank as bank_service)

router = APIRouter()

@router.get(
    "/banks",
    responses={
        200: {
            "model": Page[Bank],
            "description": "A list of banks"
        },
    },
    tags=["Bank"],
    summary="List all banks",
    response_model_by_alias=True,
)
async def banks_get(
    session: SessionDep
) -> Page[Bank]:
    return await bank_service.banks_get(session)


@router.delete(
    "/banks/{id}",
    responses={
        204: {
            "description": "Bank deleted"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Bank"],
    summary="Delete a bank",
    response_model_by_alias=True,
)
async def banks_id_delete(
    id: str,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> None:
    return await bank_service.banks_id_delete(
        id, session)


@router.get(
    "/banks/{id}",
    responses={
        200: {
            "model": Bank,
            "description": "Bank details"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Bank"],
    summary="Get a bank",
    response_model_by_alias=True,
)
async def banks_id_get(
    id: str,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> Bank:
    return await bank_service.banks_id_get(
        id, session)


@router.put(
    "/banks/{id}",
    responses={
        200: {
            "model": Bank,
            "description": "Updated bank details"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Bank"],
    summary="Update a bank",
    response_model_by_alias=True,
)
async def banks_id_put(
    id: str, bank_put: BankPut,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> Bank:
    return await bank_service.banks_id_put(
        id, bank_put, session)


@router.post(
    "/banks",
    responses={
        201: {
            "model": PostResponse,
            "description": "Base resource creation response"
        },
    },
    tags=["Bank"],
    summary="Create a bank",
    response_model_by_alias=True,
)
async def banks_post(
    banks_post: BanksPost,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> PostResponse:
    return await bank_service.banks_post(
        banks_post, session)
