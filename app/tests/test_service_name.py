from typing import Optional

import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from models import ServiceNameModel
from tests.utils import url_reverse
from tests.conftest import engine
from models.service_model import ServiceNameInSchema
from services.stub_init_service import CATEGORIES_SERVICE
from schemas.service_name_schema import ServiceNameOptionalSchema


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


def _get_service_name_schema(name: str = 'service_1', category_id: int = 1) -> ServiceNameInSchema:
    return ServiceNameInSchema(
        category_id=category_id,
        name=name,
        price=10000,
        detail='service_1 detail',
    )


@pytest.mark.parametrize(
    'schema, status_code',
    [
        (_get_service_name_schema('service_1'), status.HTTP_200_OK),
        (None, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
@pytest.mark.asyncio
async def test_post_service_name(
    async_client: AsyncClient, async_session: AsyncSession, schema: Optional[ServiceNameInSchema], status_code: int
):
    content = schema.json() if schema else '{}'
    response = await async_client.post(url_reverse('view_add_service_name'), content=content)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        result = await async_session.execute(
            select(ServiceNameModel)
            .where(
                ServiceNameModel.name == schema.name,
                ServiceNameModel.category_id == schema.category_id,
            )
            .limit(1)
        )
        service_db = result.scalars().first()
        assert service_db.name == schema.name


@pytest.mark.asyncio
async def test_post_service_name_duplicate(async_client: AsyncClient, async_session: AsyncSession):
    for i in range(1, 3):
        url = url_reverse('view_add_service_name')
        response = await async_client.post(url, content=_get_service_name_schema().json())
        status_code = status.HTTP_200_OK if i == 1 else status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.status_code == status_code


@pytest.mark.parametrize(
    'pk,data, status_code',
    [
        (1, {'name': 'new_service', 'category_id': 1}, status.HTTP_200_OK),
        (1, {}, status.HTTP_400_BAD_REQUEST),
        (100, {'name': 'new_service', 'category_id': 1}, status.HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_patch_service_name(
    async_client: AsyncClient, async_session: AsyncSession, pk: int, data: dict, status_code: int
):
    schema = ServiceNameOptionalSchema(**data)
    url = url_reverse('view_patch_service_name', pk=pk)
    response = await async_client.patch(url, content=schema.json(exclude_unset=True))
    await async_session.commit()
    assert response.status_code == status_code
    user = ServiceNameModel(**response.json())
    if status_code == status.HTTP_200_OK:
        session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with session() as s:
            category_db = await s.get(ServiceNameModel, user.id)
            assert category_db.name == schema.name
