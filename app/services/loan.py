import logging
from typing import Optional

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import select

from app.api.common.errors import (
    ResourceNotFoundError)
from app.db import SessionDep
from app.db.models import (
    Loan, LoansPost,
    TransactionsPost, TransactionType)
from app.services.transaction import transactions_post

_log = logging.getLogger(__name__)


async def _get_loan_from_db(
    id: str, session: SessionDep
) -> Loan:
    loan = session.get(Loan, id)
    if not loan:
        raise ResourceNotFoundError(resource_id=id)
    return loan


def _build_loan_transaction(
    loan: LoansPost
) -> TransactionsPost:
    loan_transaction = TransactionsPost(
        amount=loan.amount,
        description='Accredito prestito',
        type=TransactionType.DEPOSIT,
        destinationAccountId=loan.bank_account_id
    )
    return loan_transaction


async def loans_get(
    session: SessionDep,
    bank_account_id: Optional[str]
) -> Page[Loan]:
    loans_query = select(Loan)

    if bank_account_id:
        loans_query = loans_query \
            .where(Loan.bank_account_id == bank_account_id)

    return paginate(session, loans_query)


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
    loan_transaction = _build_loan_transaction(
        loans_post)
    await transactions_post(loan_transaction, session)
    session.add(loan)
    session.commit()
    session.refresh(loan)
    return loan
