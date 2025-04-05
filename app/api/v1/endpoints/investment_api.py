from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Query

from app.api.common.schemas.response import (
    MessageResponse, PostResponse)
from app.core.jwt import get_current_active_user
from app.db import SessionDep
from app.db.models import (
    Investment, InvestmentsPost,
    InvestmentActionPost, UserProfile)
from app.services import investment as investment_service

router = APIRouter()

@router.get(
    "/investments",
    responses={
        200: {
            "model": List[Investment],
            "description": "A list of investments"
        },
    },
    tags=["Investment"],
    summary="List all investments",
    response_model_by_alias=True,
)
async def investments_get(
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)],
    bank_account_id: Optional[str] = Query(None, description="", alias="bankAccountId"),
) -> List[Investment]:
    return await investment_service.investments_get(
        session, bank_account_id)


@router.post(
    "/investments/{id}/action",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Action successfully performed response"
        },
        400: {
            "model": MessageResponse,
            "description": "Action successfully performed response"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Investment"],
    summary="Perform an action on an investment",
    response_model_by_alias=True,
)
async def investments_id_action_post(
    id: str,
    investment_action_post: InvestmentActionPost,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> MessageResponse:
    return await investment_service.investments_id_action_post(
        id, investment_action_post, session)


@router.get(
    "/investments/{id}",
    responses={
        200: {
            "model": Investment,
            "description": "Investment details"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Investment"],
    summary="Get an investment",
    response_model_by_alias=True,
)
async def investments_id_get(
    id: str,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> Investment:
    return await investment_service.investments_id_get(
        id, session)


@router.post(
    "/investments",
    responses={
        201: {
            "model": PostResponse,
            "description": "Base resource creation response"
        },
    },
    tags=["Investment"],
    summary="Create an investment",
    response_model_by_alias=True,
)
async def investments_post(
    investments_post: InvestmentsPost,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> PostResponse:
    return await investment_service.investments_post(
        investments_post, session)
