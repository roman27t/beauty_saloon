from enum import Enum

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import OfferLinkModel
from routers.consts import RouteSlug
from models.database import get_session
from models.offer_model import OfferLinkInSchema
from routers.offer_routers import OfferFilter
from schemas.offer_schema import OfferLinkOptionalSchema
from services.service_service import OfferLinkService
from dependencies.offer_dependency import valid_patch_id, valid_patch_schema

router_offer_full = APIRouter()
OFFER_SERVICE = '/offer/full/'


from sqlalchemy import select


@router_offer_full.get(OFFER_SERVICE + RouteSlug.ifilter + RouteSlug.pk, response_model=list)
async def view_filter_offer_full(ifilter: OfferFilter, pk: int, session: AsyncSession = Depends(get_session)):
    params = {f'{ifilter.value}_id': pk}
    if ifilter.value == OfferFilter.service_name.value:
        params['is_active'] = True

    conditions = [getattr(OfferLinkModel, key) == value for key, value in params.items()]
    result = await session.execute(select(OfferLinkModel).where(*conditions))
    data_db = result.scalars().all()
    if not data_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return [i.dict() for i in data_db]
