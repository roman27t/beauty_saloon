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
from models.order_model import OrderInSchema
from routers.choices import OrderFilter
from services.stub_init_service import T_BOOK_DATE


@pytest.mark.parametrize(
    'field, pk, len_content, status_code',
    [
        (OrderFilter.employee.value, 1, 14, status.HTTP_200_OK),
        # (OrderFilter.client.value, 1, 15, status.HTTP_200_OK),
        # ('qwe', 1, 0, status.HTTP_422_UNPROCESSABLE_ENTITY),
        # (OrderFilter.employee.value, 999, 0, status.HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_filter_order(
    async_client: AsyncClient, async_session: AsyncSession, field, pk: int, len_content: int, status_code: int
):
    response = await async_client.get(url_reverse('view_filter_order_full', ifilter=field, pk=pk))
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        content = response.json()
        # assert len(content) == len_content
        # assert OrderModel(**content[0])
