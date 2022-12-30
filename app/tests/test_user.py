import datetime as dt
import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from models import EmployeeModel
from models.user_model import Gender, EmployeeInSchema
from routers.employee_routers import ROUTE_EMPLOYEE
from services.stub_init_service import LAST_NAMES


@pytest.mark.asyncio
async def test_get_employee_all(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.get(ROUTE_EMPLOYEE)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 5
    assert EmployeeModel(**content[0])


@pytest.mark.asyncio
async def test_get_employee_by_id(async_client: AsyncClient, async_session: AsyncSession):
    result = await async_session.execute(select(EmployeeModel).where(EmployeeModel.last_name==LAST_NAMES[0]).limit(1))
    user = result.scalars().first()
    response = await async_client.get(f'{ROUTE_EMPLOYEE}{user.id}/')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_post_employee(async_client: AsyncClient, async_session: AsyncSession):
    last_name = 'Dobruden'
    employee_schema = EmployeeInSchema(
        phone='+380983827777',
        email='employee@gmail.com',
        last_name='Dobruden',
        first_name='Hanna',
        birth_date=dt.datetime.strptime('10.02.1989', '%d.%m.%Y'),
        gender=Gender.FEMALE,
    )
    response = await async_client.post(ROUTE_EMPLOYEE, content=employee_schema.json())
    assert response.status_code == 200
    result = await async_session.execute(select(EmployeeModel).where(EmployeeModel.last_name == last_name).limit(1))
    user = result.scalars().first()
    assert user.last_name == last_name
