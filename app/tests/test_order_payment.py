from typing import Optional

import pytest
from httpx import AsyncClient
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from models import OrderModel
from tests.utils import url_reverse
from models.choices import StatusOrder
from models.order_model import OrderInSchema
from schemas.order_schema import OrderPaymentSchema
from schemas.payment_schema import CardSchema, PaymentType
from services.order_service import OrderService


def _get_order_schema(price: int, cvv: str) -> OrderPaymentSchema:
    item = CardSchema(number='4000000000000002', cvv=cvv, expire='1024')
    return OrderPaymentSchema(
        price=price,
        p_type=PaymentType.CARD,
        item=item,
    )


@pytest.mark.parametrize(
    'schema, status_code',
    [
        (_get_order_schema(price=10000, cvv='777'), status.HTTP_200_OK),  # success payment
        (_get_order_schema(price=10000, cvv='111'), status.HTTP_409_CONFLICT),  # error payment
        (None, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
@pytest.mark.asyncio
async def test_post_order_payment(
    async_client: AsyncClient, async_session: AsyncSession, schema: Optional[OrderInSchema], status_code: int
):
    _id = 1
    content = schema.json() if schema else '{}'
    response = await async_client.post(url_reverse('view_order_payment', pk=_id), content=content)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        obj_db: OrderModel = await OrderService(db_session=async_session).get(pk=_id)
        assert obj_db.status == StatusOrder.PAID
