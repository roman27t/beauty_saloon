import pytest
from httpx import AsyncClient
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from tests.utils import url_reverse
from entities.offer.schemas_offer import OfferFullResponseSchema
from entities.offer.routers_offer import OfferFilter


@pytest.mark.parametrize(
    'field, pk, len_content, status_code',
    [
        (OfferFilter.employee.value, 1, 9, status.HTTP_200_OK),
        (OfferFilter.service_name.value, 1, 5, status.HTTP_200_OK),
        ('qwe', 1, 0, status.HTTP_422_UNPROCESSABLE_ENTITY),
        (OfferFilter.employee.value, 999, 0, status.HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_filter_offer_full(
    async_client: AsyncClient, async_session: AsyncSession, field, pk: int, len_content: int, status_code: int
):
    response = await async_client.get(url_reverse('view_filter_offer_full', ifilter=field, pk=pk))
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        response_obj = OfferFullResponseSchema(**response.json())
        assert len(response_obj.offers) == len_content
        assert response_obj.employee.id == pk
        assert response_obj.categories[response_obj.offers[0].service.category_id]
