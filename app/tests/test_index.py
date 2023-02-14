import pytest
from httpx import AsyncClient
from fastapi import status

from tests.utils import url_reverse


@pytest.mark.asyncio
async def test_index(async_client: AsyncClient):
    response = await async_client.get(url_reverse('view_index'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'ok': True}


@pytest.mark.asyncio
async def test_swagger_openapi(async_client: AsyncClient):
    response = await async_client.get('/openapi.json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()
