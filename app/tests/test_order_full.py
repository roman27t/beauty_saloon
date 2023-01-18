import pytest
from httpx import AsyncClient
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from routers.order_routers import ORDER_PAGE_SIZE
from schemas.order_schema import OrderFullResponseSchema
from tests.utils import url_reverse
from routers.choices import OrderFilter


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
    response = await async_client.get(url_reverse('view_filter_order_full', ifilter=field, pk=pk))
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        response_obj = OrderFullResponseSchema(**response.json())
        assert len(response_obj.orders) == ORDER_PAGE_SIZE
        assert response_obj.user.id == pk
        service = response_obj.services[response_obj.orders[0].service_id]
        assert response_obj.categories[service.category_id]
        assert response_obj.pagination.max_rows == len_content
        assert response_obj.pagination.max_page == 3
        assert response_obj.pagination.page == 1



@pytest.mark.parametrize(
    'field, pk, page, status_code',
    [
        (OrderFilter.employee.value, 1, 1, status.HTTP_200_OK),
        (OrderFilter.client.value, 1, 1, status.HTTP_200_OK),
        (OrderFilter.employee.value, 1, 2, status.HTTP_200_OK),
        (OrderFilter.client.value, 1, 2, status.HTTP_200_OK),
        (OrderFilter.employee.value, 1, 3, status.HTTP_200_OK),
        (OrderFilter.client.value, 1, 3, status.HTTP_200_OK),
        (OrderFilter.employee.value, 1, 4, status.HTTP_404_NOT_FOUND),
        (OrderFilter.client.value, 1, 4, status.HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_filter_order_pages(
    async_client: AsyncClient, async_session: AsyncSession, field, pk: int, page: int, status_code: int
):
    main_url = url_reverse('view_filter_order_full', ifilter=field, pk=pk)
    response = await async_client.get(f'{main_url}?page={page}')
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        response_obj = OrderFullResponseSchema(**response.json())
        assert len(response_obj.orders) <= ORDER_PAGE_SIZE
        assert response_obj.user.id == pk
        order = response_obj.orders[0]
        service = response_obj.services[order.service_id]
        assert response_obj.categories[service.category_id]
        assert response_obj.pagination.max_page == 3
        assert response_obj.pagination.page == page
        ifilter: OrderFilter = OrderFilter(field)
        user_id = f'{ifilter.invert()}_id'
        assert response_obj.users[getattr(order, user_id)]
