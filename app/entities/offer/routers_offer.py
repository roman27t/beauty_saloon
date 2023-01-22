from enum import Enum

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from entities.offer.models_offer import OfferLinkModel
from entities.service_name.models_service_name import ServiceNameModel
from routers.consts import RouteSlug
from models.database import get_session
from entities.offer.models_offer import OfferLinkInSchema
from entities.offer.schemas_offer import (
    OfferFullResponseSchema,
    OfferLinkOptionalSchema,
)
from services.service_service import OfferLinkService
from dependencies.base_dependency import (
    ValidGetByIdDependency,
    valid_empty_schema,
)

router_offer = APIRouter()
R_OFFER = '/offer/'


class OfferFilter(str, Enum):
    employee = 'employee'
    service_name = 'service_name'

    def get_filters(self, pk: int) -> dict:
        params = {f'{self.value}_id': pk}
        if self.value == OfferFilter.service_name:
            params['is_active'] = True
        return params


@router_offer.get(R_OFFER + RouteSlug.ifilter + RouteSlug.pk, response_model=list[OfferLinkModel])
async def view_filter_offer(ifilter: OfferFilter, pk: int, session: AsyncSession = Depends(get_session)):
    offers = await OfferLinkService(db_session=session).filter(params=ifilter.get_filters(pk=pk))
    if not offers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return offers


@router_offer.get(R_OFFER + RouteSlug.full + RouteSlug.ifilter + RouteSlug.pk, response_model=OfferFullResponseSchema)
async def view_filter_offer_full(ifilter: OfferFilter, pk: int, session: AsyncSession = Depends(get_session)):
    joins = [
        joinedload(OfferLinkModel.employee),
        selectinload(OfferLinkModel.service_name).joinedload(ServiceNameModel.category),
    ]
    offers = await OfferLinkService(db_session=session).filter(params=ifilter.get_filters(pk=pk), options=joins)
    if not offers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return OfferFullResponseSchema.build(offers=offers)


@router_offer.post(R_OFFER, response_model=OfferLinkModel)
async def view_add_offer(schema: OfferLinkInSchema, session: AsyncSession = Depends(get_session)):
    return await OfferLinkService(db_session=session).add(schema=schema)


@router_offer.patch(R_OFFER + RouteSlug.pk, response_model=OfferLinkModel)
async def view_patch_offer(
    schema: OfferLinkOptionalSchema = Depends(valid_empty_schema(class_schema=OfferLinkOptionalSchema)),
    obj_db: OfferLinkModel = Depends(ValidGetByIdDependency(class_service=OfferLinkService)),
    session: AsyncSession = Depends(get_session),
):
    await OfferLinkService(db_session=session).update(obj_db=obj_db, schema=schema)
    return obj_db


@router_offer.delete(R_OFFER + RouteSlug.pk, response_model=OfferLinkModel)
async def view_delete_offer(
    obj_db: OfferLinkModel = Depends(ValidGetByIdDependency(class_service=OfferLinkService)),
    session: AsyncSession = Depends(get_session),
):
    schema = OfferLinkOptionalSchema(is_active=False)
    await OfferLinkService(db_session=session).update(obj_db=obj_db, schema=schema)
    return obj_db
