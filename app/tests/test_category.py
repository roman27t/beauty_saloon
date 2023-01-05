import pytest
from httpx import AsyncClient
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from models import CategoryModel
from models.service_model import CategoryInSchema
from tests.utils import url_reverse
from services.stub_init_service import CATEGORIES


@pytest.mark.asyncio
async def test_get_category_all(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.get(url_reverse('view_get_category_all'))
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == len(CATEGORIES)
    assert CategoryModel(**content[0])


@pytest.mark.parametrize('pk,status_code', [(1, status.HTTP_200_OK), (999, status.HTTP_404_NOT_FOUND)])
@pytest.mark.asyncio
async def test_get_category_by_id(
    async_client: AsyncClient, async_session: AsyncSession, pk: int, status_code: int
):
    response = await async_client.get(url_reverse('view_get_category_by_id', pk=pk))
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        category = CategoryModel(**response.json())
        assert category.name == CATEGORIES[0]


@pytest.mark.parametrize(
    'is_error, status_code',
    [
        (False, status.HTTP_200_OK),
        (True, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
@pytest.mark.asyncio
async def test_post_category(
    async_client: AsyncClient, async_session: AsyncSession, is_error: bool, status_code: int
):
    schema = CategoryInSchema(**{'name': 'test_category', 'detail': 'detail'})
    content = '{}' if is_error else schema.json()
    response = await async_client.post(url_reverse('view_add_category'), content=content)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        result = await async_session.execute(
            select(CategoryModel).where(CategoryModel.name == schema.name).limit(1)
        )
        user_db = result.scalars().first()
        assert user_db.name == schema.name


@pytest.mark.asyncio
async def test_post_category_duplicate(async_client: AsyncClient, async_session: AsyncSession):
    schema = CategoryInSchema(**{'name': 'test_category', 'detail': 'detail'})
    for i in range(1, 3):
        url = url_reverse('view_add_category')
        response = await async_client.post(url, content=schema.json())
        status_code = status.HTTP_200_OK if i == 1 else status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.status_code == status_code
