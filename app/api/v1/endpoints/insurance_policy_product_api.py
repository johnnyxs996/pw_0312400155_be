from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.api.common.schemas.response import (
    MessageResponse, PostResponse)
from app.core.jwt import get_current_active_user
from app.db import SessionDep
from app.db.models import (
    InsurancePolicyProduct, InsurancePolicyProductsPost,
    InsurancePolicyProductPut, UserProfile)
from app.services import (
    insurance_policy_product as insurance_policy_product_service)

router = APIRouter()

@router.get(
    "/insurancePolicyProducts",
    responses={
        200: {
            "model": List[InsurancePolicyProduct],
            "description": "A list of insurance policy products"
        },
    },
    tags=["Insurance Policy Product"],
    summary="List all insurance policy products",
    response_model_by_alias=True,
)
async def insurance_policy_products_get(
    session: SessionDep
) -> List[InsurancePolicyProduct]:
    return await insurance_policy_product_service.insurance_policy_products_get(
        session)


@router.delete(
    "/insurancePolicyProducts/{id}",
    responses={
        204: {"description": "Insurance policy product deleted"},
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Insurance Policy Product"],
    summary="Delete an insurance policy product",
    response_model_by_alias=True,
)
async def insurance_policy_products_id_delete(
    id: str,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> None:
    return await insurance_policy_product_service.insurance_policy_products_id_delete(
        id, session)


@router.get(
    "/insurancePolicyProducts/{id}",
    responses={
        200: {
            "model": InsurancePolicyProduct,
            "description": "Insurance Policy Product details"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Insurance Policy Product"],
    summary="Get an insurance policy product",
    response_model_by_alias=True,
)
async def insurance_policy_products_id_get(
    id: str,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> InsurancePolicyProduct:
    return await insurance_policy_product_service.insurance_policy_products_id_get(
        id, session)


@router.put(
    "/insurancePolicyProducts/{id}",
    responses={
        200: {
            "model": InsurancePolicyProduct,
            "description": "Updated insurance policy product details"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Insurance Policy Product"],
    summary="Update an insurance policy product",
    response_model_by_alias=True,
)
async def insurance_policy_products_id_put(
    id: str,
    insurance_policy_product_put: InsurancePolicyProductPut,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> InsurancePolicyProduct:
    return await insurance_policy_product_service.insurance_policy_products_id_put(
        id, insurance_policy_product_put, session)


@router.post(
    "/insurancePolicyProducts",
    responses={
        201: {
            "model": PostResponse,
            "description": "Base resource creation response"
        },
    },
    tags=["Insurance Policy Product"],
    summary="Create an insurance policy product",
    response_model_by_alias=True,
)
async def insurance_policy_products_post(
    insurance_policy_products_post: InsurancePolicyProductsPost,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> PostResponse:
    return await insurance_policy_product_service.insurance_policy_products_post(
        insurance_policy_products_post, session)
