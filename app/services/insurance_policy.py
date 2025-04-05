import logging
from typing import List, Optional

from sqlmodel import select

from app.api.common.errors import ResourceNotFoundError, OperationAmountTooLargeError, ResourceAlreadyInStatusError
from app.api.common.schemas.response import (
    MessageResponse)
from app.db import SessionDep
from app.db.models import (
    BankAccount, InsurancePolicy, InsurancePolicyAction,
    InsurancePolicyActionPost, InsurancePolicyStatus,
    InsurancePoliciesPost, InsurancePolicyProduct)
from app.services.bank_account import _get_bank_account_from_db
from app.services.insurance_policy_product import _get_insurance_policy_product_from_db

_log = logging.getLogger(__name__)


INSURANCE_POLICY_STATUS_BY_ACTION_MAP = {
    InsurancePolicyAction.REACTIVATE.value: InsurancePolicyStatus.ACTIVE,
    InsurancePolicyAction.SUSPEND.value: InsurancePolicyStatus.SUSPENDED
}


async def _get_insurance_policy_from_db(
    id: str, session: SessionDep
) -> InsurancePolicy:
    insurance_policy = session.get(
        InsurancePolicy, id)
    if not insurance_policy:
        raise ResourceNotFoundError(resource_id=id)
    return insurance_policy


async def _get_bank_account_with_updated_balance_by_insurance_policy(
    insurance_policy: InsurancePolicy,
    session: SessionDep
) -> BankAccount:
    async def _validate_insurance_policy_product_amount(
        insurance_policy_product: InsurancePolicyProduct,
        bank_account: BankAccount
    ) -> None:
        if insurance_policy_product.annual_premium > bank_account.balance:
            raise OperationAmountTooLargeError(
                available_amount=bank_account.balance)
        return

    bank_account = await _get_bank_account_from_db(
        insurance_policy.bank_account_id, session)
    insurance_policy_product = await _get_insurance_policy_product_from_db(
        insurance_policy.insurance_policy_product_id, session)

    await _validate_insurance_policy_product_amount(
        insurance_policy_product, bank_account)

    bank_account.balance -= insurance_policy_product.annual_premium

    return bank_account


async def insurance_policies_get(
    session: SessionDep,
    bank_account_id: Optional[str]
) -> List[InsurancePolicy]:
    insurance_policies_query = select(InsurancePolicy)

    if bank_account_id:
        insurance_policies_query = insurance_policies_query \
            .where(InsurancePolicy.bank_account_id == bank_account_id)

    return session.exec(insurance_policies_query).all()


async def insurance_policies_id_action_post(
    id: str,
    insurance_policy_action_post: InsurancePolicyActionPost,
    session: SessionDep
) -> MessageResponse:
    insurance_policy = await _get_insurance_policy_from_db(
        id, session)
    insurance_policy_action = insurance_policy_action_post.action

    updated_status = INSURANCE_POLICY_STATUS_BY_ACTION_MAP.get(
        insurance_policy_action)

    if insurance_policy.status_id == updated_status:
        raise ResourceAlreadyInStatusError(
            status=updated_status)

    insurance_policy.status_id = updated_status
    session.add(insurance_policy)
    session.commit()
    session.refresh(insurance_policy)
    return MessageResponse(
        message=f"Action {insurance_policy_action.value} successfully performed on resource {id}"
    )


async def insurance_policies_id_get(
    id: str,
    session: SessionDep
) -> InsurancePolicy:
    return await _get_insurance_policy_from_db(
        id, session)


async def insurance_policies_post(
    insurance_policies_post: InsurancePoliciesPost,
    session: SessionDep
) -> InsurancePolicy:
    insurance_policy = InsurancePolicy(
        **insurance_policies_post.dict(by_alias=True))
    updated_bank_account = await _get_bank_account_with_updated_balance_by_insurance_policy(
        insurance_policy, session)
    session.add(insurance_policy)
    session.add(updated_bank_account)
    session.commit()
    session.refresh(insurance_policy)
    session.refresh(updated_bank_account)
    return insurance_policy
