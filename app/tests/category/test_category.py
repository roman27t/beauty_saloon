import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from tests.utils import url_reverse
from tests.conftest import engine
from services.stub_init_service import CATEGORIES
from entities.category.models_category import CategoryModel, CategoryInSchema
from entities.category.schemas_category import CategoryOptionalSchema


@pytest.mark.asyncio
async def test_get_category_all(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.get(url_reverse('view_get_category_all'))
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == len(CATEGORIES)
    assert CategoryModel(**content[0])


@pytest.mark.parametrize('pk,status_code', [(1, status.HTTP_200_OK), (999, status.HTTP_404_NOT_FOUND)])
@pytest.mark.asyncio
async def test_get_category_by_id(async_client: AsyncClient, async_session: AsyncSession, pk: int, status_code: int):
    response = await async_client.get(url_reverse('view_get_category_by_id', pk=pk))
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        category = CategoryModel(**response.json())
        assert category.name == CATEGORIES[0]


def _get_category_schema() -> CategoryInSchema:
    return CategoryInSchema(**{'name': 'test_category', 'detail': 'detail'})


@pytest.mark.parametrize(
    'is_error, status_code',
    [
        (False, status.HTTP_200_OK),
        (True, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
@pytest.mark.asyncio
async def test_post_category(async_client: AsyncClient, async_session: AsyncSession, is_error: bool, status_code: int):
    schema = _get_category_schema()
    content = '{}' if is_error else schema.json()
    response = await async_client.post(url_reverse('view_add_category'), content=content)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        result = await async_session.execute(select(CategoryModel).where(CategoryModel.name == schema.name).limit(1))
        category_db = result.scalars().first()
        assert category_db.name == schema.name


@pytest.mark.asyncio
async def test_post_category_duplicate(async_client: AsyncClient, async_session: AsyncSession):
    for i in range(1, 3):
        url = url_reverse('view_add_category')
        response = await async_client.post(url, content=_get_category_schema().json())
        status_code = status.HTTP_200_OK if i == 1 else status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.status_code == status_code


@pytest.mark.parametrize(
    'pk,data, status_code',
    [
        (1, {'detail': 'detail'}, status.HTTP_200_OK),
        (1, {}, status.HTTP_400_BAD_REQUEST),
        (100, {'detail': 'detail'}, status.HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_patch_category(
    async_client: AsyncClient, async_session: AsyncSession, pk: int, data: dict, status_code: int
):
    schema = CategoryOptionalSchema(**data)
    url = url_reverse('view_patch_category', pk=pk)
    response = await async_client.patch(url, content=schema.json(exclude_unset=True))
    await async_session.commit()
    assert response.status_code == status_code
    user = CategoryModel(**response.json())
    if status_code == status.HTTP_200_OK:
        session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with session() as s:
            category_db = await s.get(CategoryModel, user.id)
            assert category_db.detail == schema.detail
