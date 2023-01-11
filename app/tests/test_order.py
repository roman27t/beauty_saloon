from typing import Optional

import datetime as dt
import pytest
from httpx import AsyncClient
from fastapi import status
from models.order_model import OrderInSchema
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from models import OrderModel
from tests.utils import url_reverse
from tests.conftest import engine


def  _get_order_schema(employee_id: int, service_id) -> OrderInSchema:
    return OrderInSchema(
        employee_id=employee_id,
        service_id=service_id,
        client_id=1,
        price='1000',
        comment=f'comment_{dt.datetime.now().isoformat()}',
        start_at=dt.datetime.strptime('22.08.2023 10:00', '%d.%m.%Y %H:%M'),
        end_at=dt.datetime.strptime('22.08.2023 11:00', '%d.%m.%Y %H:%M'),
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

# InternalError("(sqlalchemy.dialects.postgresql.asyncpg.InternalServerError) <class 'asyncpg.exceptions.InternalServerError'>: cache lookup failed for type 56340")
@pytest.mark.skip('todo')
@pytest.mark.asyncio
async def test_post_order_duplicate(async_client: AsyncClient, async_session: AsyncSession):
    for i in range(1, 3):
        url = url_reverse('view_add_order')
        schema = _get_order_schema(employee_id=3, service_id=1)
        # result = await async_session.execute(
        #     select(OrderModel)
        #         .where(
        #         OrderModel.employee_id == schema.employee_id,
        #         OrderModel.start_at == schema.start_at,
        #         OrderModel.end_at == schema.end_at,
        #     )
        # )
        # obj_db = result.scalars().all()

        response = await async_client.post(url, content=schema.json())
        status_code = status.HTTP_200_OK if i == 1 else status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.status_code == status_code
