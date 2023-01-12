from typing import Optional

import datetime as dt
import pytest
from httpx import AsyncClient
from fastapi import status

from models.choices import StatusOrder
from models.order_model import OrderInSchema
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from models import OrderModel
from tests.utils import url_reverse
from tests.conftest import engine


def  _get_order_schema(employee_id: int, service_id, time_start='10:00', time_end='11:00') -> OrderInSchema:
    return OrderInSchema(
        employee_id=employee_id,
        service_id=service_id,
        client_id=1,
        price='1000',
        comment=f'comment_{dt.datetime.now().isoformat()}',
        start_at=dt.datetime.strptime(f'22.08.2023 {time_start}', '%d.%m.%Y %H:%M'),
        end_at=dt.datetime.strptime(f'22.08.2023 {time_end}', '%d.%m.%Y %H:%M'),
    )


@pytest.mark.parametrize(
    'schema, status_code',
    [
        ( _get_order_schema(employee_id=1, service_id=1), status.HTTP_200_OK),
        (None, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
@pytest.mark.asyncio
async def test_post_order(
    async_client: AsyncClient, async_session: AsyncSession, schema: Optional[OrderInSchema], status_code: int
):
    content = schema.json() if schema else '{}'
    response = await async_client.post(url_reverse('view_add_order'), content=content)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        result = await async_session.execute(
            select(OrderModel)
            .where(
                OrderModel.employee_id == schema.employee_id,
                OrderModel.start_at == schema.start_at,
                OrderModel.end_at == schema.end_at,
            )
            .limit(1)
        )
        obj_db: OrderModel = result.scalars().first()
        assert obj_db.comment == schema.comment

@pytest.mark.asyncio
async def test_post_order_duplicate(async_client: AsyncClient, async_session: AsyncSession):
    for i in range(1, 3):
        schema = _get_order_schema(employee_id=3, service_id=1)
        result = await async_session.execute(
            select(OrderModel)
                .where(
                OrderModel.employee_id == schema.employee_id,
                OrderModel.start_at == schema.start_at,
                OrderModel.end_at == schema.end_at,
            )
        )
        obj_db = result.scalars().all()
        count_result = 0 if i == 1 else 1
        assert len(obj_db) == count_result
        response = await async_client.post(url_reverse('view_add_order'), content=schema.json())
        status_code = status.HTTP_200_OK if i == 1 else status.HTTP_409_CONFLICT
        assert response.status_code == status_code


@pytest.mark.parametrize(
    'pk,status_code',
    [
        (1, status.HTTP_200_OK),
        (100, status.HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_delete_order(async_client: AsyncClient, async_session: AsyncSession, pk: int, status_code: int):
    response = await async_client.delete(url_reverse('view_delete_order', pk=pk))
    await async_session.commit()
    assert response.status_code == status_code
    obj_response = OrderModel(**response.json())
    if status_code == status.HTTP_200_OK:
        session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with session() as s:
            obj_db: OrderModel = await s.get(OrderModel, obj_response.id)
            assert obj_db.status == StatusOrder.CANCEL
