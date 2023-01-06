import pytest
from httpx import AsyncClient
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from models import ServiceNameModel
from models.service_model import ServiceNameInSchema
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


def _get_service_name_schema() -> ServiceNameInSchema:
    return ServiceNameInSchema(
        category_id=1,
        name='service_1',
        price=10000,
        detail='service_1 detail',
    )


@pytest.mark.parametrize(
    'is_error, status_code',
    [
        (False, status.HTTP_200_OK),
        (True, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
@pytest.mark.asyncio
async def test_post_service_name(
    async_client: AsyncClient, async_session: AsyncSession, is_error: bool, status_code: int
):
    schema = _get_service_name_schema()
    content = '{}' if is_error else schema.json()
    response = await async_client.post(url_reverse('view_add_service_name'), content=content)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        result = await async_session.execute(
            select(ServiceNameModel).where(
                ServiceNameModel.name == schema.name,
                ServiceNameModel.category_id == schema.category_id,
            ).limit(1)
        )
        service_db = result.scalars().first()
        assert service_db.name == schema.name
