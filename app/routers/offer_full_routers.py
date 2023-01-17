from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from models import OfferLinkModel, ServiceNameModel
from routers.consts import RouteSlug
from models.database import get_session
from routers.offer_routers import OfferFilter
from schemas.offer_schema import OfferFullResponseSchema

router_offer_full = APIRouter()
OFFER_SERVICE = '/offer/full/'


@router_offer_full.get(OFFER_SERVICE + RouteSlug.ifilter + RouteSlug.pk, response_model=OfferFullResponseSchema)
async def view_filter_offer_full(ifilter: OfferFilter, pk: int, session: AsyncSession = Depends(get_session)):
    params = {f'{ifilter.value}_id': pk}
    if ifilter.value == OfferFilter.service_name.value:
        params['is_active'] = True
    conditions = [getattr(OfferLinkModel, key) == value for key, value in params.items()]
    result = await session.execute(
        select(OfferLinkModel)
        .where(*conditions)
        .options(
            selectinload(OfferLinkModel.employee),
            selectinload(OfferLinkModel.service_name).selectinload(ServiceNameModel.category),
        )
    )
    data_db = result.scalars().all()
    if not data_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return OfferFullResponseSchema.build(data_db=data_db)
