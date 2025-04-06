from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.api.common.schemas.response import (
    MessageResponse, PostResponse)
from app.core.jwt import get_current_active_user
from app.db import SessionDep
from app.db.models import (
    InvestmentProduct, InvestmentProductPut,
    InvestmentProductsPost, UserProfile)
from app.services import (
    investment_product as investment_product_service)

router = APIRouter()

@router.get(
    "/investmentProducts",
    responses={
        200: {
            "model": List[InvestmentProduct],
            "description": "A list of investment products"
        },
    },
    tags=["Investment Product"],
    summary="List all investment products",
    response_model_by_alias=True,
)
async def investment_products_get(
    session: SessionDep
) -> List[InvestmentProduct]:
    return await investment_product_service.investment_products_get(
        session)


@router.delete(
    "/investmentProducts/{id}",
    responses={
        204: {"description": "Investment product deleted"},
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Investment Product"],
    summary="Delete an investment product",
    response_model_by_alias=True,
)
async def investment_products_id_delete(
    id: str,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> None:
    return await investment_product_service.investment_products_id_delete(
        id, session)


@router.get(
    "/investmentProducts/{id}",
    responses={
        200: {
            "model": InvestmentProduct,
            "description": "Investment Product details"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Investment Product"],
    summary="Get an investment product",
    response_model_by_alias=True,
)
async def investment_products_id_get(
    id: str,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> InvestmentProduct:
    return await investment_product_service.investment_products_id_get(
        id, session)


@router.put(
    "/investmentProducts/{id}",
    responses={
        200: {
            "model": InvestmentProduct,
            "description": "Updated investment product details"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Investment Product"],
    summary="Update an investment product",
    response_model_by_alias=True,
)
async def investment_products_id_put(
    id: str,
    investment_product_put: InvestmentProductPut,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> InvestmentProduct:
    return await investment_product_service.investment_products_id_put(
        id, investment_product_put, session)


@router.post(
    "/investmentProducts",
    responses={
        201: {
            "model": PostResponse,
            "description": "Base resource creation response"
        },
    },
    tags=["Investment Product"],
    summary="Create an investment product",
    response_model_by_alias=True,
)
async def investment_products_post(
    investment_products_post: InvestmentProductsPost,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> PostResponse:
    return await investment_product_service.investment_products_post(
        investment_products_post, session)
