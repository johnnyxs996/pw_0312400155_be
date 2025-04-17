from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page

from app.api.common.schemas.response import (
    MessageResponse, PostResponse)
from app.core.jwt import get_current_active_user
from app.db import SessionDep
from app.db.models import (
    InsurancePolicy, InsurancePoliciesPost,
    InsurancePolicyActionPost, UserProfile)
from app.services import (
    insurance_policy as insurance_policy_service)

router = APIRouter()

@router.get(
    "/insurancePolicies",
    responses={
        200: {
            "model": Page[InsurancePolicy],
            "description": "A list of insurance policies"
        },
    },
    tags=["Insurance Policy"],
    summary="List all insurance policies",
    response_model_by_alias=True,
)
async def insurance_policies_get(
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)],
    bank_account_id: Optional[str] = Query(None, description="", alias="bankAccountId")
) -> Page[InsurancePolicy]:
    return await insurance_policy_service.insurance_policies_get(
        session, bank_account_id)


@router.post(
    "/insurancePolicies/{id}/action",
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
    tags=["Insurance Policy"],
    summary="Perform an action on an insurance policy",
    response_model_by_alias=True,
)
async def insurance_policies_id_action_post(
    id: str,
    insurance_policy_action_post: InsurancePolicyActionPost,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> MessageResponse:
    return await insurance_policy_service.insurance_policies_id_action_post(
        id, insurance_policy_action_post, session)


@router.get(
    "/insurancePolicies/{id}",
    responses={
        200: {
            "model": InsurancePolicy,
            "description": "Insurance Policy details"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Insurance Policy"],
    summary="Get an insurance policy",
    response_model_by_alias=True,
)
async def insurance_policies_id_get(
    id: str,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> InsurancePolicy:
    return await insurance_policy_service.insurance_policies_id_get(
        id, session)


@router.post(
    "/insurancePolicies",
    responses={
        201: {
            "model": PostResponse,
            "description": "Base resource creation response"
        },
    },
    tags=["Insurance Policy"],
    summary="Create an insurance policy",
    response_model_by_alias=True,
)
async def insurance_policies_post(
    insurance_policies_post: InsurancePoliciesPost,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> PostResponse:
    return await insurance_policy_service.insurance_policies_post(
        insurance_policies_post, session)
