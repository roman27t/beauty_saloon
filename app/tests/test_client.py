import datetime as dt
import pytest
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from fastapi import status
from models import ClientModel
from models.user_model import ClientInSchema, ClientInOptionalSchema
from models.choices import Gender
from services.stub_init_service import LAST_NAMES
from tests.conftest import engine
from tests.utils import url_reverse


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


@pytest.mark.asyncio
async def test_post_client(async_client: AsyncClient, async_session: AsyncSession):
    last_name = 'Dobruden'
    employee_schema = ClientInSchema(
        phone='+380983827777',
        email='employee@gmail.com',
        last_name=last_name,
        first_name='Hanna',
        birth_date=dt.datetime.strptime('10.02.1989', '%d.%m.%Y'),
        gender=Gender.FEMALE,
    )
    response = await async_client.post(url_reverse('view_add_client'), content=employee_schema.json())
    assert response.status_code == status.HTTP_200_OK
    result = await async_session.execute(select(ClientModel).where(ClientModel.last_name == last_name).limit(1))
    user = result.scalars().first()
    assert user.last_name == last_name


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
