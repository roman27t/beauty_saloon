from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import ServiceNameModel
from models.database import get_session
from routers.category_routers import ROUTE_CATEGORY
from services.service_service import ServiceNameService
from schemas.service_name_schema import ServiceNameOptionalSchema
from dependencies.service_name_dependency import (
    valid_patch_id,
    valid_patch_schema,
)

router_service = APIRouter()
ROUTE_SERVICE = '/service/'
ROUTE_SERVICE_CATEGORY = f'{ROUTE_SERVICE}{ROUTE_CATEGORY[1:]}'


@router_service.get(ROUTE_SERVICE, response_model=list[ServiceNameModel])
async def view_get_service_name_all(session: AsyncSession = Depends(get_session)):
    return await ServiceNameService(db_session=session).get_all()


@router_service.get(ROUTE_SERVICE + '{pk}/', response_model=ServiceNameModel)
async def view_get_service_name_by_id(pk: int, session: AsyncSession = Depends(get_session)):
    category = await ServiceNameService(db_session=session).get(pk=pk)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return category


@router_service.get(ROUTE_SERVICE_CATEGORY + '{pk}/', response_model=list[ServiceNameModel])
async def view_filter_service_name(pk: int, session: AsyncSession = Depends(get_session)):
    services = await ServiceNameService(db_session=session).filter({'category_id': pk})
    if not services:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return services


@router_service.post(ROUTE_SERVICE, response_model=ServiceNameModel)
async def view_add_service_name(client: ServiceNameModel, session: AsyncSession = Depends(get_session)):
    return await ServiceNameService(db_session=session).add(schema=client)


@router_service.patch(ROUTE_SERVICE + '{pk}/', response_model=ServiceNameModel)
async def view_patch_service_name(
    schema: ServiceNameOptionalSchema = Depends(valid_patch_schema),
    obj_db: ServiceNameModel = Depends(valid_patch_id),
    session: AsyncSession = Depends(get_session),
):
    await ServiceNameService(db_session=session).update(obj_db=obj_db, schema=schema)
    return obj_db
