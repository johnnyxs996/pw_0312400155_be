from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.api.common.schemas.response import (
    MessageResponse, PostResponse)
from app.core.jwt import get_current_active_user
from app.db import SessionDep
from app.db.models import (
    LoanProduct, LoanProductPut,
    LoanProductsPost, UserProfile)
from app.services import (
    loan_product as loan_product_service)

router = APIRouter()

@router.get(
    "/loanProducts",
    responses={
        200: {
            "model": List[LoanProduct],
            "description": "A list of loan products"
        },
    },
    tags=["Loan Product"],
    summary="List all loan products",
    response_model_by_alias=True,
)
async def loan_products_get(
    session: SessionDep
) -> List[LoanProduct]:
    return await loan_product_service.loan_products_get(
        session)


@router.delete(
    "/loanProducts/{id}",
    responses={
        204: {"description": "Loan product deleted"},
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Loan Product"],
    summary="Delete a loan product",
    response_model_by_alias=True,
)
async def loan_products_id_delete(
    id: str,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> None:
    return await loan_product_service.loan_products_id_delete(
        id, session)


@router.get(
    "/loanProducts/{id}",
    responses={
        200: {
            "model": LoanProduct,
            "description": "Loan Product details"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Loan Product"],
    summary="Get a loan product",
    response_model_by_alias=True,
)
async def loan_products_id_get(
    id: str,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> LoanProduct:
    return await loan_product_service.loan_products_id_get(
        id, session)


@router.put(
    "/loanProducts/{id}",
    responses={
        200: {
            "model": LoanProduct,
            "description": "Updated loan product details"
        },
        404: {
            "model": MessageResponse,
            "description": "Resource not found response"
        },
    },
    tags=["Loan Product"],
    summary="Update a loan product",
    response_model_by_alias=True,
)
async def loan_products_id_put(
    id: str,
    loan_product_put: LoanProductPut,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> LoanProduct:
    return await loan_product_service.loan_products_id_put(
        id, loan_product_put, session)


@router.post(
    "/loanProducts",
    responses={
        201: {
            "model": PostResponse,
            "description": "Base resource creation response"
        },
    },
    tags=["Loan Product"],
    summary="Create a loan product",
    response_model_by_alias=True,
)
async def loan_products_post(
    loan_products_post: LoanProductsPost,
    session: SessionDep,
    authenticated_user_profile: Annotated[UserProfile, Depends(get_current_active_user)]
) -> PostResponse:
    return await loan_product_service.loan_products_post(
        loan_products_post, session)
