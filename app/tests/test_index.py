import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.mark.asyncio
async def test_index(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.get('/')
    assert response.status_code == 200
    assert response.json() == {'ok': True}


@pytest.mark.asyncio
async def test_1(async_client: AsyncClient, async_session: AsyncSession):
    # response = await async_client.post("/items/1", json=payload,)
    response = await async_client.get("/items/1")

    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "q": None}
