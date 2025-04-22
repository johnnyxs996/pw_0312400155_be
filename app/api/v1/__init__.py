from fastapi import APIRouter

from .endpoints import (
    auth_api, bank_account_api, bank_api,
    insurance_policy_api,
    insurance_policy_product_api, investment_api,
    investment_product_api, loan_api,
    loan_product_api, transaction_api,
    user_bank_account_api, user_profile_api)


api_router = APIRouter()

api_router.include_router(auth_api.router, prefix='/auth')
api_router.include_router(bank_account_api.router)
api_router.include_router(bank_api.router)
api_router.include_router(insurance_policy_api.router)
api_router.include_router(insurance_policy_product_api.router)
api_router.include_router(investment_api.router)
api_router.include_router(investment_product_api.router)
api_router.include_router(loan_api.router)
api_router.include_router(loan_product_api.router)
api_router.include_router(transaction_api.router)
api_router.include_router(user_bank_account_api.router)
api_router.include_router(user_profile_api.router)
