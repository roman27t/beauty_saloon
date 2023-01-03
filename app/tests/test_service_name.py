import pytest
from httpx import AsyncClient
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from models import ServiceNameModel
from tests.utils import url_reverse
from services.stub_init_service import CATEGORIES_SERVICE


@pytest.mark.asyncio
async def test_get_service_name_all(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.get(url_reverse('view_get_service_name_all'))
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == sum([len(i) for i in CATEGORIES_SERVICE.values()])
    assert ServiceNameModel(**content[0])


@pytest.mark.parametrize('pk,status_code', [(1, status.HTTP_200_OK), (999, status.HTTP_404_NOT_FOUND)])
@pytest.mark.asyncio
async def test_get_service_name_by_id(
    async_client: AsyncClient, async_session: AsyncSession, pk: int, status_code: int
):
    response = await async_client.get(url_reverse('view_get_service_name_by_id', pk=pk))
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        service = ServiceNameModel(**response.json())
        assert service.name == tuple(CATEGORIES_SERVICE.values())[0][0]


@pytest.mark.parametrize('pk,status_code', [(1, status.HTTP_200_OK), (999, status.HTTP_404_NOT_FOUND)])
@pytest.mark.asyncio
async def test_filter_service_name_by_id(
    async_client: AsyncClient, async_session: AsyncSession, pk: int, status_code: int
):
    response = await async_client.get(url_reverse('view_filter_service_name', pk=pk))
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        content = response.json()
        assert len(content) == len(tuple(CATEGORIES_SERVICE.values())[0])
        assert ServiceNameModel(**content[0])
