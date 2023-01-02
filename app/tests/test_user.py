import datetime as dt
import pytest
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from models import EmployeeModel
from models.user_model import EmployeeInSchema, EmployeeInOptionalSchema
from models.choices import Gender
from services.stub_init_service import LAST_NAMES
from tests.conftest import engine
from tests.utils import url_reverse


@pytest.mark.asyncio
async def test_get_employee_all(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.get(url_reverse('view_get_employee_all'))
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 5
    assert EmployeeModel(**content[0])


@pytest.mark.parametrize('pk,status_code', [(1, 200), (999, 404)])
@pytest.mark.asyncio
async def test_get_employee_by_id(async_client: AsyncClient, async_session: AsyncSession, pk: int, status_code: int):
    response = await async_client.get(url_reverse('view_get_employee_by_id', pk=pk))
    assert response.status_code == status_code
    if status_code == 200:
        employee = EmployeeModel(**response.json())
        assert employee.last_name == LAST_NAMES[0]


@pytest.mark.asyncio
async def test_post_employee(async_client: AsyncClient, async_session: AsyncSession):
    last_name = 'Dobruden'
    employee_schema = EmployeeInSchema(
        phone='+380983827777',
        email='employee@gmail.com',
        last_name=last_name,
        first_name='Hanna',
        birth_date=dt.datetime.strptime('10.02.1989', '%d.%m.%Y'),
        gender=Gender.FEMALE,
    )
    response = await async_client.post(url_reverse('view_add_employee'), content=employee_schema.json())
    assert response.status_code == 200
    result = await async_session.execute(select(EmployeeModel).where(EmployeeModel.last_name == last_name).limit(1))
    user = result.scalars().first()
    assert user.last_name == last_name


@pytest.mark.parametrize(
    'pk,schema, status_code',
    [
        (1, EmployeeInOptionalSchema(first_name='Katerina'), 200),
        (1, EmployeeInOptionalSchema(), 400),
        (100, EmployeeInOptionalSchema(first_name='Katerina'), 404),
    ],
)
@pytest.mark.asyncio
async def test_patch_employee(
        async_client: AsyncClient,
        async_session: AsyncSession,
        pk: int,
        schema: EmployeeInOptionalSchema,
        status_code: int
):
    url = url_reverse('view_patch_employee', pk=pk)
    response = await async_client.patch(url, content=schema.json(exclude_unset=True))
    await async_session.commit()
    assert response.status_code == status_code
    employee = EmployeeModel(**response.json())
    if status_code == 200:
        session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with session() as s:
            user = await s.get(EmployeeModel, employee.id)
            assert user.first_name == schema.first_name
