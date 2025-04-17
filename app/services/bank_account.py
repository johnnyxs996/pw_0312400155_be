import logging

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import select

from app.api.common.errors import ResourceNotFoundError
from app.db import SessionDep
from app.db.models import BankAccount, BankAccountPut

_log = logging.getLogger(__name__)

async def _get_bank_account_from_db(
    id: str, session: SessionDep
) -> BankAccount:
    bank_account = session.get(BankAccount, id)
    if not bank_account:
        raise ResourceNotFoundError(resource_id=id)
    return bank_account


async def bank_accounts_get(
    session: SessionDep
) -> Page[BankAccount]:
    return paginate(session, select(BankAccount))


async def bank_accounts_id_delete(
    id: str,
    session: SessionDep
) -> None:
    bank_account = await _get_bank_account_from_db(
        id, session)
    session.delete(bank_account)
    session.commit()
    return None


async def bank_accounts_id_get(
    id: str,
    session: SessionDep
) -> BankAccount:
    return await _get_bank_account_from_db(
        id, session)


async def bank_accounts_id_put(
    id: str,
    bank_account_put: BankAccountPut,
    session: SessionDep
) -> BankAccount:
    bank_account = await _get_bank_account_from_db(
        id, session)
    bank_account_update_data = bank_account_put.model_dump(
        exclude_unset=True)
    bank_account.sqlmodel_update(bank_account_update_data)
    session.add(bank_account)
    session.commit()
    session.refresh(bank_account)
    return bank_account
