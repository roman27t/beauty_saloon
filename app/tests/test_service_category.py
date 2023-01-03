import pytest
from httpx import AsyncClient
from fastapi import status
from models import ServiceCategoryModel
from sqlmodel.ext.asyncio.session import AsyncSession

from services.stub_init_service import CATEGORIES
from tests.utils import url_reverse


@pytest.mark.asyncio
async def test_get_service_category_all(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.get(url_reverse('view_get_service_category_all'))
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == len(CATEGORIES)
    assert ServiceCategoryModel(**content[0])


@pytest.mark.parametrize('pk,status_code', [(1, status.HTTP_200_OK), (999, status.HTTP_404_NOT_FOUND)])
@pytest.mark.asyncio
async def test_get_user_by_id(async_client: AsyncClient, async_session: AsyncSession, pk: int, status_code: int):
    response = await async_client.get(url_reverse('view_get_service_category_by_id', pk=pk))
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        category = ServiceCategoryModel(**response.json())
        assert category.name == CATEGORIES[0]
