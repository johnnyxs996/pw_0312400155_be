import logging

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.api.common.errors import (
    ResourceNotFoundError, DuplicateKeyError)
from app.db import SessionDep
from app.db.models import (
    CredentialsPut, User, UserProfile,
    UserProfilesPost, UserProfileWithUserData)
from app.utils.secrets import get_password_hash

_log = logging.getLogger(__name__)


async def _get_user_from_db(
    id: str, session: SessionDep
) -> User:
    user = session.get(User, id)
    if not user:
        raise ResourceNotFoundError(
            resource_id=id)
    return user


async def _get_user_profile_from_db(
    id: str, session: SessionDep
) -> UserProfile:
    user_profile = session.get(UserProfile, id)
    if not user_profile:
        raise ResourceNotFoundError(
            resource_id=id)
    return user_profile


async def _get_full_user_profile_from_db(
    id: str, session: SessionDep
) -> UserProfileWithUserData:
    user_profile_query = select(UserProfile, User) \
        .where(UserProfile.id == id) \
        .join(User, User.id == UserProfile.user_id)
    user_profile_with_user = session.exec(
        user_profile_query).first()
    if not user_profile_with_user:
        raise ResourceNotFoundError(
            resource_id=id)
    user_profile = user_profile_with_user[0]
    user = user_profile_with_user[1]
    return UserProfileWithUserData.model_validate(
        dict(
            id=user_profile.id,
            email=user_profile.email,
            last_login=user_profile.last_login,
            created_at=user_profile.created_at,
            name=user.name,
            surname=user.surname,
            tax_identification_number=user.tax_identification_number,
            birth_date=user.birth_date,
            birth_country=user.birth_country,
            birth_state=user.birth_state,
            birth_city=user.birth_city
        )
    )


async def user_profiles_get(
    session: SessionDep
) -> Page[UserProfile]:
    return paginate(session, select(UserProfile))


async def user_profiles_id_delete(
    id: str,
    session: SessionDep
) -> None:
    user_profile = await _get_user_profile_from_db(id, session)
    user = await _get_user_from_db(user_profile.user_id, session)
    session.delete(user_profile)
    session.delete(user)
    session.commit()
    return None


async def user_profiles_id_get(
    id: str,
    session: SessionDep
) -> UserProfileWithUserData:
    user_profile = await _get_full_user_profile_from_db(id, session)
    return user_profile


async def user_profiles_id_put(
    id: str,
    user_profile_put: CredentialsPut,
    session: SessionDep
) -> UserProfileWithUserData:
    user_profile = await _get_user_profile_from_db(id, session)
    updated_user_profile = user_profile_put.model_dump(
        exclude_unset=True)
    user_profile.sqlmodel_update(updated_user_profile)
    session.add(user_profile)
    session.commit()
    session.refresh(user_profile)
    full_user_profile = await _get_full_user_profile_from_db(
        id, session)
    return full_user_profile


async def user_profiles_post(
    user_profiles_post: UserProfilesPost,
    session: SessionDep
) -> UserProfile:
    def _create_user(
        user_profiles_post: UserProfilesPost,
        session: SessionDep
    ) -> User:
        user = User(**user_profiles_post.dict(by_alias=True))

        session.add(user)
        return user

    # TODO: aggiungere verifica su constraint
    user = _create_user(user_profiles_post, session)

    user_profile = UserProfile.model_validate(
        dict(
            email=user_profiles_post.email,
            password=get_password_hash(
                user_profiles_post.password),
            user_id=user.id))
    try:
        session.add(user_profile)
        session.commit()
        session.refresh(user)
        session.refresh(user_profile)
    except IntegrityError:
        session.rollback()
        raise DuplicateKeyError()
    return user_profile
