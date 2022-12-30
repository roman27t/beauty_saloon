import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from models import EmployeeModel
from routers.employee_routers import ROUTE_EMPLOYEE


@pytest.mark.asyncio
async def test_employee(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.get(ROUTE_EMPLOYEE)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 5
    assert EmployeeModel(**content[0])
