import pytest
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from fastapi import status
from models import ClientModel
from schemas.user_schemas import ClientInSchema, ClientInOptionalSchema
from services.stub_init_service import LAST_NAMES
from tests.conftest import engine
from tests.utils import url_reverse, user_data


@pytest.mark.asyncio
async def test_get_client_all(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.get(url_reverse('view_get_client_all'))
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 5
    assert ClientModel(**content[0])


@pytest.mark.parametrize('pk,status_code', [(1, status.HTTP_200_OK), (999, status.HTTP_404_NOT_FOUND)])
@pytest.mark.asyncio
async def test_get_client_by_id(async_client: AsyncClient, async_session: AsyncSession, pk: int, status_code: int):
    response = await async_client.get(url_reverse('view_get_client_by_id', pk=pk))
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        employee = ClientModel(**response.json())
        assert employee.last_name == LAST_NAMES[5]


@pytest.mark.parametrize(
    'is_error, status_code',
    [
        (False, status.HTTP_200_OK),
        (True, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
@pytest.mark.asyncio
async def test_post_client(async_client: AsyncClient, async_session: AsyncSession, is_error: bool, status_code: int):
    employee_schema = ClientInSchema(**user_data())
    content = '{}' if is_error else employee_schema.json()
    response = await async_client.post(url_reverse('view_add_client'), content=content)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        result = await async_session.execute(
            select(ClientModel).where(ClientModel.last_name == employee_schema.last_name).limit(1)
        )
        user = result.scalars().first()
        assert user.last_name == employee_schema.last_name


@pytest.mark.asyncio
async def test_post_client_duplicate(async_client: AsyncClient, async_session: AsyncSession):
    for i in range(1,3):
        response = await async_client.post(url_reverse('view_add_client'), content=ClientInSchema(**user_data()).json())
        status_code = status.HTTP_200_OK if i == 1 else status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.status_code == status_code


@pytest.mark.parametrize(
    'pk,schema, status_code',
    [
        (1, ClientInOptionalSchema(first_name='Katerina'), status.HTTP_200_OK),
        (1, ClientInOptionalSchema(), status.HTTP_400_BAD_REQUEST),
        (100, ClientInOptionalSchema(first_name='Katerina'), status.HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_patch_client(
        async_client: AsyncClient,
        async_session: AsyncSession,
        pk: int,
        schema: ClientInOptionalSchema,
        status_code: int
):
    url = url_reverse('view_patch_client', pk=pk)
    response = await async_client.patch(url, content=schema.json(exclude_unset=True))
    await async_session.commit()
    assert response.status_code == status_code
    employee = ClientModel(**response.json())
    if status_code == status.HTTP_200_OK:
        session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with session() as s:
            user = await s.get(ClientModel, employee.id)
            assert user.first_name == schema.first_name
