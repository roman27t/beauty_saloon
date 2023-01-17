from enum import Enum

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from models import OfferLinkModel, ServiceNameModel
from routers.consts import RouteSlug
from models.database import get_session
from models.offer_model import OfferLinkInSchema
from schemas.offer_schema import OfferLinkOptionalSchema, OfferFullResponseSchema
from services.service_service import OfferLinkService
from dependencies.offer_dependency import valid_patch_id, valid_patch_schema

router_offer = APIRouter()
R_OFFER = '/offer/'


class OfferFilter(str, Enum):
    employee = 'employee'
    service_name = 'service_name'


@router_offer.get(R_OFFER + RouteSlug.ifilter + RouteSlug.pk, response_model=list[OfferLinkModel])
async def view_filter_offer(ifilter: OfferFilter, pk: int, session: AsyncSession = Depends(get_session)):
    params = {f'{ifilter.value}_id': pk}
    if ifilter.value == OfferFilter.service_name.value:
        params['is_active'] = True
    offers = await OfferLinkService(db_session=session).filter(params)
    if not offers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return offers


@router_offer.get(R_OFFER + RouteSlug.full + RouteSlug.ifilter + RouteSlug.pk, response_model=OfferFullResponseSchema)
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


@router_offer.post(R_OFFER, response_model=OfferLinkModel)
async def view_add_offer(schema: OfferLinkInSchema, session: AsyncSession = Depends(get_session)):
    return await OfferLinkService(db_session=session).add(schema=schema)


@router_offer.patch(R_OFFER + RouteSlug.pk, response_model=OfferLinkModel)
async def view_patch_offer(
    schema: OfferLinkOptionalSchema = Depends(valid_patch_schema),
    obj_db: OfferLinkModel = Depends(valid_patch_id),
    session: AsyncSession = Depends(get_session),
):
    await OfferLinkService(db_session=session).update(obj_db=obj_db, schema=schema)
    return obj_db


@router_offer.delete(R_OFFER + RouteSlug.pk, response_model=OfferLinkModel)
async def view_delete_offer(
    obj_db: OfferLinkModel = Depends(valid_patch_id),
    session: AsyncSession = Depends(get_session),
):
    schema = OfferLinkOptionalSchema(is_active=False)
    await OfferLinkService(db_session=session).update(obj_db=obj_db, schema=schema)
    return obj_db
