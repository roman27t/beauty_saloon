from enum import Enum

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import OfferLinkModel
from routers.consts import RouteSlug
from models.database import get_session
from models.offer_model import OfferLinkInSchema
from schemas.offer_schema import OfferLinkOptionalSchema
from services.service_service import OfferLinkService
from dependencies.offer_dependency import valid_patch_id, valid_patch_schema

offer_service = APIRouter()
OFFER_SERVICE = '/offer/'


class OfferFilter(str, Enum):
    employee = 'employee'
    service_name = 'service_name'


@offer_service.get(OFFER_SERVICE + RouteSlug.ifilter + RouteSlug.pk, response_model=list[OfferLinkModel])
async def view_filter_offer(ifilter: OfferFilter, pk: int, session: AsyncSession = Depends(get_session)):
    params = {f'{ifilter.value}_id': pk}
    if ifilter.value == OfferFilter.service_name.value:
        params['is_active'] = True
    offers = await OfferLinkService(db_session=session).filter(params)
    if not offers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return offers


@offer_service.post(OFFER_SERVICE, response_model=OfferLinkModel)
async def view_add_offer(schema: OfferLinkInSchema, session: AsyncSession = Depends(get_session)):
    return await OfferLinkService(db_session=session).add(schema=schema)


@offer_service.patch(OFFER_SERVICE + RouteSlug.pk, response_model=OfferLinkModel)
async def view_patch_offer(
    schema: OfferLinkOptionalSchema = Depends(valid_patch_schema),
    obj_db: OfferLinkModel = Depends(valid_patch_id),
    session: AsyncSession = Depends(get_session),
):
    await OfferLinkService(db_session=session).update(obj_db=obj_db, schema=schema)
    return obj_db


@offer_service.delete(OFFER_SERVICE + RouteSlug.pk, response_model=OfferLinkModel)
async def view_delete_offer(
    obj_db: OfferLinkModel = Depends(valid_patch_id),
    session: AsyncSession = Depends(get_session),
):
    schema = OfferLinkOptionalSchema(is_active=False)
    await OfferLinkService(db_session=session).update(obj_db=obj_db, schema=schema)
    return obj_db
