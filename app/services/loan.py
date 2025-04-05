import logging
from typing import List, Optional

from sqlmodel import select

from app.api.common.errors import (
    ResourceNotFoundError, OperationAmountTooLargeError)
from app.db import SessionDep
from app.db.models import (
    BankAccount, Loan, LoansPost)
from app.services.bank_account import _get_bank_account_from_db

_log = logging.getLogger(__name__)


async def _get_loan_from_db(
    id: str, session: SessionDep
) -> Loan:
    loan = session.get(Loan, id)
    if not loan:
        raise ResourceNotFoundError(resource_id=id)
    return loan


async def _get_bank_account_with_updated_balance_by_loan(
    loan: Loan,
    session: SessionDep
) -> BankAccount:
    bank_account = await _get_bank_account_from_db(
            loan.bank_account_id, session)

    bank_account.balance += loan.amount

    return bank_account


async def loans_get(
    session: SessionDep,
    bank_account_id: Optional[str]
) -> List[Loan]:
    loans_query = select(Loan)

    if bank_account_id:
        loans_query = loans_query \
            .where(Loan.bank_account_id == bank_account_id)

    return session.exec(loans_query).all()


async def loans_id_get(
    id: str,
    session: SessionDep
) -> Loan:
    return await _get_loan_from_db(
        id, session)


async def loans_post(
    loans_post: LoansPost,
    session: SessionDep
) -> Loan:
    loan = Loan(
        **loans_post.dict(by_alias=True))
    updated_bank_account = await _get_bank_account_with_updated_balance_by_loan(
        loan, session)
    session.add(loan)
    session.add(updated_bank_account)
    session.commit()
    session.refresh(loan)
    session.refresh(updated_bank_account)
    return loan
