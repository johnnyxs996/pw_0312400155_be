import logging
from typing import List, Optional

from sqlmodel import select

from app.api.common.errors import ResourceNotFoundError, OperationAmountTooLargeError, ResourceAlreadyInStatusError
from app.api.common.schemas.response import (
    MessageResponse)
from app.db import SessionDep
from app.db.models import (
    BankAccount, Investment, InvestmentsPost,
    InvestmentAction, InvestmentStatus,
    InvestmentActionPost)
from app.services.bank_account import _get_bank_account_from_db

_log = logging.getLogger(__name__)


INVESTMENT_STATUS_BY_ACTION_MAP = {
    InvestmentAction.ACTIVATE.value: InvestmentStatus.ACTIVE,
    InvestmentAction.CLOSE.value: InvestmentStatus.CLOSED
}


async def _get_investment_from_db(
    id: str, session: SessionDep
) -> Investment:
    investment = session.get(
        Investment, id)
    if not investment:
        raise ResourceNotFoundError(resource_id=id)
    return investment


async def _get_bank_account_with_updated_balance_by_investment(
    investment: Investment,
    session: SessionDep
) -> BankAccount:
    async def _validate_investment_amount(
        investment: Investment,
        bank_account: BankAccount
    ) -> None:
        if investment.amount > bank_account.balance:
            raise OperationAmountTooLargeError(
                available_amount=bank_account.balance)
        return

    bank_account = await _get_bank_account_from_db(
            investment.bank_account_id, session)

    await _validate_investment_amount(investment, bank_account)

    bank_account.balance -= investment.amount

    return bank_account


async def investments_get(
    session: SessionDep,
    bank_account_id: Optional[str]
) -> List[Investment]:
    investments_query = select(Investment)

    if bank_account_id:
        investments_query = investments_query \
            .where(Investment.bank_account_id == bank_account_id)

    return session.exec(investments_query).all()


async def investments_id_action_post(
    id: str,
    investment_action_post: InvestmentActionPost,
    session: SessionDep
) -> MessageResponse:
    investment = await _get_investment_from_db(
        id, session)
    investment_action = investment_action_post.action

    updated_status = INVESTMENT_STATUS_BY_ACTION_MAP.get(
        investment_action)

    if investment.status_id == updated_status:
        raise ResourceAlreadyInStatusError(
            status=updated_status)

    investment.status_id = updated_status
    session.add(investment)
    session.commit()
    session.refresh(investment)
    return MessageResponse(
        message=f"Action {investment_action.value} successfully performed on resource {id}"
    )


async def investments_id_get(
    id: str,
    session: SessionDep
) -> Investment:
    return await _get_investment_from_db(
        id, session)


async def investments_post(
    investments_post: InvestmentsPost,
    session: SessionDep
) -> Investment:
    investment = Investment(
        **investments_post.dict(by_alias=True))
    updated_bank_account = await _get_bank_account_with_updated_balance_by_investment(
        investment, session)
    session.add(investment)
    session.add(updated_bank_account)
    session.commit()
    session.refresh(investment)
    session.refresh(updated_bank_account)
    return investment
