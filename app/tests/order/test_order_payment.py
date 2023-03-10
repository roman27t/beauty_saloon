from typing import Optional

import pytest
from httpx import AsyncClient
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from tests.utils import url_reverse
from entities.order.models_order import OrderModel, OrderInSchema
from entities.order.choices_order import StatusOrder
from entities.order.services_order import OrderService
from entities.order.schemas.schema_order import OrderPaymentSchema
from entities.order.schemas.schema_payment import CardSchema, PaymentType


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
        (_get_order_schema(price=9999, cvv='777'), status.HTTP_409_CONFLICT),  # error payment - bad price
        (_get_order_schema(price=10000, cvv='111'), status.HTTP_409_CONFLICT),  # error payment - api error
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
