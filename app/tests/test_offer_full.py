from typing import Optional

import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from models import OfferLinkModel
from tests.utils import url_reverse
from tests.conftest import engine
from models.offer_model import OfferLinkInSchema
from schemas.offer_schema import OfferLinkOptionalSchema
from routers.offer_routers import OfferFilter


@pytest.mark.parametrize(
    'field, pk, len_content, status_code',
    [
        (OfferFilter.employee.value, 1, 9, status.HTTP_200_OK),
        # (OfferFilter.service_name.value, 1, 5, status.HTTP_200_OK),
        # ('qwe', 1, 0, status.HTTP_422_UNPROCESSABLE_ENTITY),
        # (OfferFilter.employee.value, 999, 0, status.HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_filter_offer_full(
    async_client: AsyncClient, async_session: AsyncSession, field, pk: int, len_content: int, status_code: int
):
    response = await async_client.get(url_reverse('view_filter_offer_full', ifilter=field, pk=pk))
    assert response.status_code == status_code
    # if status_code == status.HTTP_200_OK:
    #     content = response.json()
    #     assert len(content) == len_content
    #     assert OfferLinkModel(**content[0])
