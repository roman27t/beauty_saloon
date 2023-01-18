import datetime as dt
from typing import Optional

import pytest
from httpx import AsyncClient
from fastapi import status
from freezegun import freeze_time
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from models import OrderModel
from tests.utils import url_reverse
from models.choices import StatusOrder
from tests.conftest import MOCK_FREEZE_TIME, engine
from routers.choices import OrderFilter
from models.order_model import OrderInSchema
from services.stub_init_service import T_BOOK_DATE


@pytest.mark.parametrize(
    'field, pk, len_content, status_code',
    [
        (OrderFilter.employee.value, 1, 14, status.HTTP_200_OK),
        (OrderFilter.client.value, 1, 15, status.HTTP_200_OK),
        ('qwe', 1, 0, status.HTTP_422_UNPROCESSABLE_ENTITY),
        (OrderFilter.employee.value, 999, 0, status.HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_filter_order(
    async_client: AsyncClient, async_session: AsyncSession, field, pk: int, len_content: int, status_code: int
):
    response = await async_client.get(url_reverse('view_filter_order', ifilter=field, pk=pk))
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        content = response.json()
        assert len(content) == len_content
        assert OrderModel(**content[0])


def _get_order_schema(
    employee_id: int,
    service_id,
    price: int,
    date_start='22.08.2023',
    date_end='22.08.2023',
    time_start='10:00',
    time_end='11:00',
) -> OrderInSchema:
    return OrderInSchema(
        employee_id=employee_id,
        service_id=service_id,
        client_id=1,
        price=price,
        comment=f'comment_{dt.datetime.now().isoformat()}',
        start_at=dt.datetime.strptime(f'{date_start} {time_start}', '%d.%m.%Y %H:%M'),
        end_at=dt.datetime.strptime(f'{date_end} {time_end}', '%d.%m.%Y %H:%M'),
    )


@freeze_time(MOCK_FREEZE_TIME)
@pytest.mark.parametrize(
    'schema, status_code',
    [
        (_get_order_schema(employee_id=1, service_id=1, price=10000), status.HTTP_200_OK),
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


@freeze_time(MOCK_FREEZE_TIME)
@pytest.mark.asyncio
async def test_post_order_duplicate(async_client: AsyncClient, async_session: AsyncSession):
    for i in range(1, 3):
        schema = _get_order_schema(employee_id=3, service_id=1, price=12000)
        result = await async_session.execute(
            select(OrderModel).where(
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


@freeze_time(MOCK_FREEZE_TIME)
@pytest.mark.parametrize(
    'd_date, d_end, t_date, t_end, status_code',
    [
        (T_BOOK_DATE, T_BOOK_DATE, '10:00', '11:00', status.HTTP_409_CONFLICT),
        (T_BOOK_DATE, T_BOOK_DATE, '11:00', '12:00', status.HTTP_409_CONFLICT),
        (T_BOOK_DATE, T_BOOK_DATE, '11:00', '12:30', status.HTTP_409_CONFLICT),
        (T_BOOK_DATE, T_BOOK_DATE, '11:00', '15:00', status.HTTP_409_CONFLICT),
        (T_BOOK_DATE, T_BOOK_DATE, '13:00', '15:00', status.HTTP_409_CONFLICT),
        (T_BOOK_DATE, T_BOOK_DATE, '13:30', '15:00', status.HTTP_409_CONFLICT),
        (T_BOOK_DATE, T_BOOK_DATE, '12:00', '13:00', status.HTTP_200_OK),
        (T_BOOK_DATE, T_BOOK_DATE, '12:00', '14:00', status.HTTP_200_OK),
        (T_BOOK_DATE, T_BOOK_DATE, '12:00', '16:00', status.HTTP_409_CONFLICT),
        (T_BOOK_DATE, T_BOOK_DATE, '13:00', '14:00', status.HTTP_200_OK),
        (T_BOOK_DATE, T_BOOK_DATE, '13:30', '14:30', status.HTTP_409_CONFLICT),
        (T_BOOK_DATE, T_BOOK_DATE, '14:00', '15:00', status.HTTP_409_CONFLICT),
    ],
)
@pytest.mark.asyncio
async def test_post_order_validate(
    async_client: AsyncClient, async_session: AsyncSession, d_date, d_end, t_date, t_end, status_code: int
):
    schema = _get_order_schema(
        employee_id=3, service_id=1, date_start=d_date, date_end=d_end, time_start=t_date, time_end=t_end, price=12000
    )
    response = await async_client.post(url_reverse('view_add_order'), content=schema.json())
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
