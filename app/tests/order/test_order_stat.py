import pytest
from httpx import AsyncClient
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from tests.utils import url_reverse
from entities.order.choices_order import OrderFilter


@pytest.mark.parametrize(
    'field, len_content, status_code',
    [
        (OrderFilter.employee.value, 1, status.HTTP_200_OK),
        ('qwe', 1, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
@pytest.mark.asyncio
async def test_filter_order(
    async_client: AsyncClient, async_session: AsyncSession, field, len_content: int, status_code: int
):
    response = await async_client.get(url_reverse('view_order_statistic', ifilter=field))
    assert response.status_code == status_code
