import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.mark.asyncio
async def test_qwe_2(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.get("/cities/biggest")
    assert response.status_code == 201
    print(response.json())
