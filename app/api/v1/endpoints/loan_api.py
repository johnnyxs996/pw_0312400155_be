from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Query

from app.api.common.schemas.response import (
    MessageResponse, PostResponse)
from app.core.jwt import get_current_active_user
from app.db import SessionDep
from app.db.models import Loan, LoansPost, UserProfile
from app.services import loan as loan_service

router = APIRouter()

@router.get(
    "/loans",
    responses={
        200: {
            "model": List[Loan],
            "description": "A list of loans"
        },
    },
    tags=["Loan"],
    summary="List all loans",
    response_model_by_alias=True,
)
async def loans_get(
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)],
    bank_account_id: Optional[str] = Query(None, description="", alias="bankAccountId"),
) -> List[Loan]:
    return await loan_service.loans_get(
        session, bank_account_id)


@router.get(
    "/loans/{id}",
    responses={
        200: {
            "model": Loan,
            "description": "Loan details"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Loan"],
    summary="Get a loan",
    response_model_by_alias=True,
)
async def loans_id_get(
    id: str,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> Loan:
    return await loan_service.loans_id_get(
        id, session)


@router.post(
    "/loans",
    responses={
        201: {
            "model": PostResponse,
            "description": "Base resource creation response"
        },
    },
    tags=["Loan"],
    summary="Create a loan",
    response_model_by_alias=True,
)
async def loans_post(
    loans_post: LoansPost,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> PostResponse:
    return await loan_service.loans_post(
        loans_post, session)
