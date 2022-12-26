import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.mark.asyncio
async def test_index(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.get('/')
    assert response.status_code == 200
    assert response.json() == {'ok': True}
