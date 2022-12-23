import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.mark.asyncio
async def test_qwe_1(async_client: AsyncClient, async_session: AsyncSession):
   # response = await async_client.post("/items/1", json=payload,)
   response = await async_client.get("/items/1")

   assert response.status_code == 200
   assert response.json() == {'item_id': 1, 'q': None}


@pytest.mark.asyncio
async def test_qwe_2(async_client: AsyncClient, async_session: AsyncSession):
   response = await async_client.get('/cities/biggest')

   assert response.status_code == 201
   print(response.json())
