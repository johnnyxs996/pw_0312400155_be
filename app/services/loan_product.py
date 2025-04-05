import logging
from typing import List

from sqlmodel import select

from app.api.common.errors import ResourceNotFoundError
from app.db import SessionDep
from app.db.models import (
    LoanProduct, LoanProductPut,
    LoanProductsPost)

_log = logging.getLogger(__name__)

async def _get_loan_product_from_db(
    id: str, session: SessionDep
) -> LoanProduct:
    loan_product = session.get(LoanProduct, id)
    if not loan_product:
        raise ResourceNotFoundError(
            resource_id=id)
    return loan_product


async def loan_products_get(
    session: SessionDep
) -> List[LoanProduct]:
    return session.exec(select(LoanProduct)).all()


async def loan_products_id_delete(
    id: str,
    session: SessionDep
) -> None:
    loan_product = await _get_loan_product_from_db(
        id, session)
    session.delete(loan_product)
    session.commit()
    return None


async def loan_products_id_get(
    id: str,
    session: SessionDep
) -> LoanProduct:
    return await _get_loan_product_from_db(
        id, session)


async def loan_products_id_put(
    id: str,
    loan_product_put: LoanProductPut,
    session: SessionDep
) -> LoanProduct:
    loan_product = \
        await _get_loan_product_from_db(
            id, session)
    loan_product_update_data = \
        loan_product_put.model_dump(
            exclude_unset=True)
    loan_product.sqlmodel_update(
        loan_product_update_data)
    session.add(loan_product)
    session.commit()
    session.refresh(loan_product)
    return loan_product


async def loan_products_post(
    loan_products_post: LoanProductsPost,
    session: SessionDep
) -> LoanProduct:
    loan_product = LoanProduct(
        **loan_products_post.dict(by_alias=True))
    session.add(loan_product)
    session.commit()
    session.refresh(loan_product)
    return loan_product
