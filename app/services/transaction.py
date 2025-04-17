import logging
from typing import List, Optional

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import or_
from sqlmodel import select

from app.api.common.errors import ResourceNotFoundError, OperationAmountTooLargeError
from app.db import SessionDep
from app.db.models import (
    Transaction, TransactionsPost, BankAccount, TransactionType)
from app.services.bank_account import _get_bank_account_from_db

_log = logging.getLogger(__name__)

async def _get_transaction_from_db(
    id: str, session: SessionDep
) -> Transaction:
    transaction = session.get(Transaction, id)
    if not transaction:
        raise ResourceNotFoundError(
            resource_id=id)
    return transaction


async def _get_bank_accounts_with_updated_balance_by_transaction(
    transaction: Transaction,
    session: SessionDep
) -> List[BankAccount]:
    async def _validate_transaction_amount(
            transaction: Transaction,
            source_account: BankAccount
    ) -> None:
        transaction_type = transaction.type

        if transaction_type in [TransactionType.TRANSFER, TransactionType.WITHDRAW]:
            if transaction.amount > source_account.balance:
                raise OperationAmountTooLargeError(
                    available_amount=source_account.balance)
        return

    source_bank_account = None
    destination_bank_account = None
    involved_accounts = []
    if transaction.source_account_id:
        source_bank_account = await _get_bank_account_from_db(
            transaction.source_account_id, session)
    if transaction.destination_account_id:
        destination_bank_account = await _get_bank_account_from_db(
            transaction.destination_account_id, session)

    await _validate_transaction_amount(transaction, source_bank_account)

    transaction_amount = transaction.amount
    transaction_with_fee = transaction_amount + (
        transaction_amount * transaction.fee / 100)

    if transaction.type is TransactionType.TRANSFER:
        source_bank_account.balance -= transaction_with_fee
        destination_bank_account.balance += transaction_amount
    if transaction.type is TransactionType.WITHDRAW:
        source_bank_account.balance -= transaction_with_fee
    if transaction.type is TransactionType.DEPOSIT:
        destination_bank_account.balance += transaction_amount

    if source_bank_account is not None:
        involved_accounts.append(source_bank_account)
    if destination_bank_account is not None:
        involved_accounts.append(destination_bank_account)
    return involved_accounts


async def transactions_get(
    session: SessionDep,
    source_account_id: Optional[str],
    destination_account_id: Optional[str],
    involved_account_id: Optional[str]
) -> Page[Transaction]:
    transactions_query = select(Transaction)

    if involved_account_id:
        transactions_query = transactions_query.where(
            or_(
                Transaction.source_account_id == involved_account_id,
                Transaction.destination_account_id == involved_account_id))
    elif source_account_id:
        transactions_query = transactions_query \
            .where(Transaction.source_account_id == source_account_id)
    elif destination_account_id:
        transactions_query = transactions_query \
            .where(Transaction.destination_account_id == destination_account_id)

    return paginate(session, transactions_query)


async def transactions_id_get(
    id: str,
    session: SessionDep
) -> Transaction:
    return await _get_transaction_from_db(id, session)


async def transactions_post(
    transactions_post: TransactionsPost,
    session: SessionDep
) -> Transaction:
    transaction = Transaction(
        **transactions_post.dict(by_alias=True))

    updated_bank_accounts: List[BankAccount] = await _get_bank_accounts_with_updated_balance_by_transaction(
        transaction, session)

    session.add(transaction)
    for updated_bank_account in updated_bank_accounts:
        session.add(updated_bank_account)
    session.commit()
    session.refresh(transaction)
    for updated_bank_account in updated_bank_accounts:
        session.refresh(updated_bank_account)

    return transaction
