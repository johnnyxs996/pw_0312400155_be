import logging
from typing import List

from sqlmodel import select

from app.api.common.errors import ResourceNotFoundError
from app.db import SessionDep
from app.db.models import (
    InsurancePolicyProduct, InsurancePolicyProductsPost,
    InsurancePolicyProductPut)

_log = logging.getLogger(__name__)

async def _get_insurance_policy_product_from_db(
    id: str, session: SessionDep
) -> InsurancePolicyProduct:
    insurance_policy_product = session.get(
        InsurancePolicyProduct, id)
    if not insurance_policy_product:
        raise ResourceNotFoundError(resource_id=id)
    return insurance_policy_product


async def insurance_policy_products_get(
    session: SessionDep
) -> List[InsurancePolicyProduct]:
    return session.exec(select(InsurancePolicyProduct)).all()


async def insurance_policy_products_id_delete(
    id: str,
    session: SessionDep
) -> None:
    insurance_policy_product = await _get_insurance_policy_product_from_db(
        id, session)
    session.delete(insurance_policy_product)
    session.commit()
    return None


async def insurance_policy_products_id_get(
    id: str,
    session: SessionDep
) -> InsurancePolicyProduct:
    return await _get_insurance_policy_product_from_db(
        id, session)


async def insurance_policy_products_id_put(
    id: str,
    insurance_policy_product_put: InsurancePolicyProductPut,
    session: SessionDep
) -> InsurancePolicyProduct:
    insurance_policy_product = \
        await _get_insurance_policy_product_from_db(
            id, session)
    insurance_policy_product_update_data = \
        insurance_policy_product_put.model_dump(
            exclude_unset=True)
    insurance_policy_product.sqlmodel_update(
        insurance_policy_product_update_data)
    session.add(insurance_policy_product)
    session.commit()
    session.refresh(insurance_policy_product)
    return insurance_policy_product


async def insurance_policy_products_post(
    insurance_policy_products_post: InsurancePolicyProductsPost,
    session: SessionDep
) -> InsurancePolicyProduct:
    insurance_policy_product = InsurancePolicyProduct(
        **insurance_policy_products_post.dict(by_alias=True))
    session.add(insurance_policy_product)
    session.commit()
    session.refresh(insurance_policy_product)
    return insurance_policy_product
