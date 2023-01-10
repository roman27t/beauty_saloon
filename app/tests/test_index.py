import pytest
from httpx import AsyncClient
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from tests.utils import url_reverse


@pytest.mark.asyncio
async def test_index(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.get(url_reverse('view_index'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'ok': True}
