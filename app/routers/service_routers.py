from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from entities.service_name.model_service_name import ServiceNameModel
from routers.consts import RouteSlug
from models.database import get_session
from services.service_service import ServiceNameService
from schemas.service_name_schema import ServiceNameOptionalSchema
from dependencies.base_dependency import (
    ValidGetByIdDependency,
    valid_empty_schema,
)

router_service = APIRouter()
ROUTE_SERVICE = '/service/'
_ROUTE_CATEGORY = '/category/'
ROUTE_SERVICE_CATEGORY = f'{ROUTE_SERVICE}{_ROUTE_CATEGORY[1:]}'


@router_service.get(ROUTE_SERVICE, response_model=list[ServiceNameModel])
async def view_get_service_name_all(session: AsyncSession = Depends(get_session)):
    return await ServiceNameService(db_session=session).get_all()


@router_service.get(ROUTE_SERVICE + RouteSlug.pk, response_model=ServiceNameModel)
async def view_get_service_name_by_id(pk: int, session: AsyncSession = Depends(get_session)):
    return await ServiceNameService(db_session=session).get(pk=pk)


@router_service.get(ROUTE_SERVICE_CATEGORY + RouteSlug.pk, response_model=list[ServiceNameModel])
async def view_filter_service_name(pk: int, session: AsyncSession = Depends(get_session)):
    services = await ServiceNameService(db_session=session).filter({'category_id': pk})
    if not services:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return services


@router_service.post(ROUTE_SERVICE, response_model=ServiceNameModel)
async def view_add_service_name(schema: ServiceNameModel, session: AsyncSession = Depends(get_session)):
    return await ServiceNameService(db_session=session).add(schema=schema)


@router_service.patch(ROUTE_SERVICE + RouteSlug.pk, response_model=ServiceNameModel)
async def view_patch_service_name(
    schema: ServiceNameOptionalSchema = Depends(valid_empty_schema(class_schema=ServiceNameOptionalSchema)),
    obj_db: ServiceNameModel = Depends(ValidGetByIdDependency(class_service=ServiceNameService)),
    session: AsyncSession = Depends(get_session),
):
    await ServiceNameService(db_session=session).update(obj_db=obj_db, schema=schema)
    return obj_db
