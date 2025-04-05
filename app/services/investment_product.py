import logging
from typing import List

from sqlmodel import select

from app.api.common.errors import ResourceNotFoundError
from app.db import SessionDep
from app.db.models import (
    InvestmentProduct, InvestmentProductPut,
    InvestmentProductsPost)

_log = logging.getLogger(__name__)

async def _get_investment_product_from_db(
    id: str, session: SessionDep
) -> InvestmentProduct:
    investment_product = session.get(InvestmentProduct, id)
    if not investment_product:
        raise ResourceNotFoundError(
            resource_id=id)
    return investment_product


async def investment_products_get(
    session: SessionDep
) -> List[InvestmentProduct]:
    return session.exec(select(InvestmentProduct)).all()


async def investment_products_id_delete(
    id: str,
    session: SessionDep
) -> None:
    investment_product = await _get_investment_product_from_db(
        id, session)
    session.delete(investment_product)
    session.commit()
    return None


async def investment_products_id_get(
    id: str,
    session: SessionDep
) -> InvestmentProduct:
    return await _get_investment_product_from_db(
        id, session)


async def investment_products_id_put(
    id: str,
    investment_product_put: InvestmentProductPut,
    session: SessionDep
) -> InvestmentProduct:
    investment_product = \
        await _get_investment_product_from_db(
            id, session)
    investment_product_update_data = \
        investment_product_put.model_dump(
            exclude_unset=True)
    investment_product.sqlmodel_update(
        investment_product_update_data)
    session.add(investment_product)
    session.commit()
    session.refresh(investment_product)
    return investment_product


async def investment_products_post(
    investment_products_post: InvestmentProductsPost,
    session: SessionDep
) -> InvestmentProduct:
    investment_product = InvestmentProduct(
        **investment_products_post.dict(by_alias=True))
    session.add(investment_product)
    session.commit()
    session.refresh(investment_product)
    return investment_product
