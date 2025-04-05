from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Query

from app.api.common.schemas.response import (
    MessageResponse, PostResponse)
from app.core.jwt import get_current_active_user
from app.db import SessionDep
from app.db.models import (
    Transaction, TransactionsPost, UserProfile)
from app.services import (
    transaction as transaction_service)

router = APIRouter()

@router.get(
    "/transactions",
    responses={
        200: {
            "model": List[Transaction],
            "description": "A list of transactions"
        },
    },
    tags=["Transaction"],
    summary="List all transactions",
    response_model_by_alias=True,
)
async def transactions_get(
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)],
    source_account_id: Optional[str] = Query(None, description="", alias="sourceAccountId"),
    destination_account_id: Optional[str] = Query(None, description="", alias="destinationAccountId"),
    involved_account_id: Optional[str] = Query(None, description="", alias="involvedAccountId"),
) -> List[Transaction]:
    return await transaction_service.transactions_get(
        session, source_account_id, destination_account_id, involved_account_id)


@router.get(
    "/transactions/{id}",
    responses={
        200: {
            "model": Transaction,
            "description": "Transaction details"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Transaction"],
    summary="Get a transaction by ID",
    response_model_by_alias=True,
)
async def transactions_id_get(
    id: str,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> Transaction:
    return await transaction_service.transactions_id_get(
        id, session)


@router.post(
    "/transactions",
    responses={
        201: {
            "model": PostResponse,
            "description": "Base resource creation response"
        },
    },
    tags=["Transaction"],
    summary="Create a transaction",
    response_model_by_alias=True,
)
async def transactions_post(
    transactions_post: TransactionsPost,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> PostResponse:
    return await transaction_service.transactions_post(
        transactions_post, session)
