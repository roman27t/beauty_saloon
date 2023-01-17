from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from models import OfferLinkModel, ServiceNameModel
from routers.consts import RouteSlug
from models.database import get_session
from routers.offer_routers import OfferFilter
from schemas.offer_schema import OfferFullResponseSchema
from services.service_service import OfferLinkService

router_offer_full = APIRouter()
OFFER_SERVICE = '/offer/full/'


@router_offer_full.get(OFFER_SERVICE + RouteSlug.ifilter + RouteSlug.pk, response_model=OfferFullResponseSchema)
async def view_filter_offer_full(ifilter: OfferFilter, pk: int, session: AsyncSession = Depends(get_session)):
    params = {f'{ifilter.value}_id': pk}
    if ifilter.value == OfferFilter.service_name.value:
        params['is_active'] = True
    joins = [
        joinedload(OfferLinkModel.employee),
        selectinload(OfferLinkModel.service_name).joinedload(ServiceNameModel.category),
    ]
    offers = await OfferLinkService(db_session=session).filter(params=params, options=joins)
    if not offers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return OfferFullResponseSchema.build(data_db=offers)
