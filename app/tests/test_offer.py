from typing import Optional

import pytest
from httpx import AsyncClient
from fastapi import status

from models.offer_model import OfferLinkInSchema
from routers.offer_routers import OfferFilter
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from models import OfferLinkModel
from tests.utils import url_reverse
from tests.conftest import engine


@pytest.mark.parametrize('field, pk, len_content, status_code', [
    (OfferFilter.employee.value, 1, 9, status.HTTP_200_OK),
    (OfferFilter.service_name.value, 1, 5, status.HTTP_200_OK),
    ('qwe', 1, 0, status.HTTP_422_UNPROCESSABLE_ENTITY),
    (OfferFilter.employee.value, 999, 0, status.HTTP_404_NOT_FOUND),
])
@pytest.mark.asyncio
async def test_filter_offer(
    async_client: AsyncClient, async_session: AsyncSession, field, pk: int, len_content: int, status_code: int
):
    response = await async_client.get(url_reverse('view_filter_offer', field=field, pk=pk))
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        content = response.json()
        assert len(content) == len_content
        assert OfferLinkModel(**content[0])


def _get_offer_schema(employee_id:int, service_name_id) -> OfferLinkInSchema:
    return OfferLinkInSchema(
        employee_id=employee_id,
        service_name_id=service_name_id,
        rate='1.1',
    )


@pytest.mark.parametrize(
    'schema, status_code',
    [
        (_get_offer_schema(employee_id=1, service_name_id=20), status.HTTP_200_OK),
        (None, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
@pytest.mark.asyncio
async def test_post_offer(
    async_client: AsyncClient, async_session: AsyncSession, schema: Optional[OfferLinkInSchema], status_code: int
):
    content = schema.json() if schema else '{}'
    response = await async_client.post(url_reverse('view_add_offer'), content=content)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        result = await async_session.execute(
            select(OfferLinkModel)
            .where(
                OfferLinkModel.employee_id == schema.employee_id,
                OfferLinkModel.service_name_id == schema.service_name_id,
            )
            .limit(1)
        )
        service_db = result.scalars().first()
        assert service_db.service_name_id == schema.service_name_id


@pytest.mark.asyncio
async def test_post_offer_duplicate(async_client: AsyncClient, async_session: AsyncSession):
    for i in range(1, 3):
        url = url_reverse('view_add_offer')
        response = await async_client.post(url, content=_get_offer_schema(employee_id=1, service_name_id=20).json())
        status_code = status.HTTP_200_OK if i == 1 else status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.status_code == status_code


# @pytest.mark.parametrize(
#     'pk,data, status_code',
#     [
#         (1, {'name': 'new_service', 'category_id': 1}, status.HTTP_200_OK),
#         (1, {}, status.HTTP_400_BAD_REQUEST),
#         (100, {'name': 'new_service', 'category_id': 1}, status.HTTP_404_NOT_FOUND),
#     ],
# )
# @pytest.mark.asyncio
# async def test_patch_service_name(
#     async_client: AsyncClient, async_session: AsyncSession, pk: int, data: dict, status_code: int
# ):
#     schema = ServiceNameOptionalSchema(**data)
#     url = url_reverse('view_patch_service_name', pk=pk)
#     response = await async_client.patch(url, content=schema.json(exclude_unset=True))
#     await async_session.commit()
#     assert response.status_code == status_code
#     user = OfferLinkModel(**response.json())
#     if status_code == status.HTTP_200_OK:
#         session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#         async with session() as s:
#             category_db = await s.get(OfferLinkModel, user.id)
#             assert category_db.name == schema.name
