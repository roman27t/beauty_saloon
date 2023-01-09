from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import OfferLinkModel
from models.database import get_session
from routers.category_routers import ROUTE_CATEGORY
from services.service_service import OfferLinkService
from schemas.service_name_schema import ServiceNameOptionalSchema
from dependencies.service_name_dependency import (
    valid_patch_id,
    valid_patch_schema,
)

offer_service = APIRouter()
OFFER_SERVICE = '/offer/'


# @offer_service.get(OFFER_SERVICE, response_model=list[OfferLinkModel])
# async def view_get_service_name_all(session: AsyncSession = Depends(get_session)):
#     return await OfferLinkService(db_session=session).get_all()

from enum import Enum


class OfferFilter(str, Enum):
    employee = 'employee'
    service_name = 'service_name'


@offer_service.get(OFFER_SERVICE + '{field}/' + '{pk}/', response_model=list[OfferLinkModel])
async def view_filter_offer(field: OfferFilter, pk: int, session: AsyncSession = Depends(get_session)):
    offers = await OfferLinkService(db_session=session).filter({f'{field.value}_id': pk})
    if not offers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return offers


# @offer_service.get(ROUTE_SERVICE_CATEGORY + '{pk}/', response_model=list[OfferLinkModel])
# async def view_filter_service_name(pk: int, session: AsyncSession = Depends(get_session)):
#     services = await OfferLinkService(db_session=session).filter({'category_id': pk})
#     if not services:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
#     return services
# 
# 
# @offer_service.post(OFFER_SERVICE, response_model=OfferLinkModel)
# async def view_add_service_name(client: OfferLinkModel, session: AsyncSession = Depends(get_session)):
#     return await OfferLinkService(db_session=session).add(schema=client)
# 
# 
# @offer_service.patch(OFFER_SERVICE + '{pk}/', response_model=OfferLinkModel)
# async def view_patch_service_name(
#     schema: ServiceNameOptionalSchema = Depends(valid_patch_schema),
#     obj_db: OfferLinkModel = Depends(valid_patch_id),
#     session: AsyncSession = Depends(get_session),
# ):
#     await OfferLinkService(db_session=session).update(obj_db=obj_db, schema=schema)
#     return obj_db
