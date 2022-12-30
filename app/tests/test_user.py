import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from models import EmployeeModel
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
