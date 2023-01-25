from fastapi import Depends, APIRouter, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from backgrounds import task_clear_db_cache
from dependencies import ValidGetByIdDependency, valid_empty_schema
from routers.consts import RouteSlug
from models.database import get_session
from core.utils.decorators import cached
from core.utils.time_seconds import TimeSeconds
from entities.offer.models_offer import OfferLinkModel, OfferLinkInSchema
from entities.offer.choices_offer import OfferFilter
from entities.offer.schemas_offer import (
    OfferFullResponseSchema,
    OfferLinkOptionalSchema,
)
from entities.offer.services_offer import OfferLinkService
from entities.service_name.models_service_name import ServiceNameModel

router_offer = APIRouter()
R_OFFER = '/offer/'


@router_offer.get(R_OFFER + RouteSlug.ifilter + RouteSlug.pk, response_model=list[OfferLinkModel])
@cached(expire=TimeSeconds.M5, extra_keys=['pk', 'ifilter'])
async def view_filter_offer(ifilter: OfferFilter, pk: int, session: AsyncSession = Depends(get_session)):
    offers = await OfferLinkService(db_session=session).filter(params=ifilter.get_filters(pk=pk))
    if not offers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return offers


@router_offer.get(R_OFFER + RouteSlug.full + RouteSlug.ifilter + RouteSlug.pk, response_model=OfferFullResponseSchema)
@cached(expire=TimeSeconds.M5, extra_keys=['pk', 'ifilter'])
async def view_filter_offer_full(ifilter: OfferFilter, pk: int, session: AsyncSession = Depends(get_session)):
    joins = [
        joinedload(OfferLinkModel.employee),
        selectinload(OfferLinkModel.service_name).joinedload(ServiceNameModel.category),
    ]
    offer_service = OfferLinkService(db_session=session)
    params = (
        # *offer_service.parse_params(ifilter.get_filters(pk=pk)),
        OfferLinkModel.service_name.is_active==True,
    )
    print('!'*80)
    print(params)
    print('!'*80)
    offers = await offer_service.filter(params=params, options=joins)
    if not offers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return OfferFullResponseSchema.build(offers=offers)


@router_offer.post(R_OFFER, response_model=OfferLinkModel)
async def view_add_offer(
    schema: OfferLinkInSchema, background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_session)
):
    result = await OfferLinkService(db_session=session).add(schema=schema)
    background_tasks.add_task(task_clear_db_cache)
    return result


@router_offer.patch(R_OFFER + RouteSlug.pk, response_model=OfferLinkModel)
async def view_patch_offer(
    background_tasks: BackgroundTasks,
    schema: OfferLinkOptionalSchema = Depends(valid_empty_schema(class_schema=OfferLinkOptionalSchema)),
    obj_db: OfferLinkModel = Depends(ValidGetByIdDependency(class_service=OfferLinkService)),
    session: AsyncSession = Depends(get_session),
):
    await OfferLinkService(db_session=session).update(obj_db=obj_db, schema=schema)
    background_tasks.add_task(task_clear_db_cache)
    return obj_db


@router_offer.delete(R_OFFER + RouteSlug.pk, response_model=OfferLinkModel)
async def view_delete_offer(
    background_tasks: BackgroundTasks,
    obj_db: OfferLinkModel = Depends(ValidGetByIdDependency(class_service=OfferLinkService)),
    session: AsyncSession = Depends(get_session),
):
    schema = OfferLinkOptionalSchema(is_active=False)
    await OfferLinkService(db_session=session).update(obj_db=obj_db, schema=schema)
    background_tasks.add_task(task_clear_db_cache)
    return obj_db
