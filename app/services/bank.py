import logging

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import select

from app.api.common.errors import ResourceNotFoundError
from app.db import SessionDep
from app.db.models import Bank, BanksPost, BankPut

_log = logging.getLogger(__name__)


async def _get_bank_from_db(
    id: str, session: SessionDep
) -> Bank:
    bank = session.get(Bank, id)
    if not bank:
        raise ResourceNotFoundError(resource_id=id)
    return bank


async def banks_get(
    session: SessionDep
) -> Page[Bank]:
    return paginate(session, select(Bank))


async def banks_id_delete(
    id: str,
    session: SessionDep
) -> None:
    bank = await _get_bank_from_db(id, session)
    session.delete(bank)
    session.commit()
    return None


async def banks_id_get(
    id: str,
    session: SessionDep
) -> Bank:
    bank = await _get_bank_from_db(id, session)
    return bank


async def banks_id_put(
    id: str, bank_put: BankPut,
    session: SessionDep
) -> Bank:
    bank = await _get_bank_from_db(id, session)
    bank_data = bank_put.model_dump(exclude_unset=True)
    bank.sqlmodel_update(bank_data)
    session.add(bank)
    session.commit()
    session.refresh(bank)
    return bank


async def banks_post(
    banks_post: BanksPost,
    session: SessionDep
) -> Bank:
    bank = Bank(**banks_post.dict(by_alias=True))
    session.add(bank)
    session.commit()
    session.refresh(bank)
    return bank
