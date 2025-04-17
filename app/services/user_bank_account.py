import logging

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import select

from app.api.common.errors import ResourceNotFoundError
from app.db import SessionDep
from app.db.models import (
    BankAccount, BankAccountsPost, UserProfile)

_log = logging.getLogger(__name__)

async def _get_user_profile_from_db(
    id: str, session: SessionDep
) -> UserProfile:
    user_profile = session.get(UserProfile, id)
    if not user_profile:
        raise ResourceNotFoundError(
            resource_id=id)
    return user_profile


async def user_profiles_id_bank_accounts_get(
    user_profile_id: str,
    session: SessionDep
) -> Page[BankAccount]:
    user_bank_accounts_query = select(BankAccount) \
        .where(BankAccount.user_profile_id == user_profile_id)
    return paginate(session, user_bank_accounts_query)


async def user_profiles_id_bank_accounts_post(
    user_profile_id: str,
    bank_accounts_post: BankAccountsPost,
    session: SessionDep
) -> BankAccount:
    _ = await _get_user_profile_from_db(user_profile_id, session)
    bank_account = BankAccount(
        **bank_accounts_post.dict(by_alias=True),
        userProfileId=user_profile_id
    )
    session.add(bank_account)
    session.commit()
    session.refresh(bank_account)
    return bank_account
