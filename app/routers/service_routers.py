from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import ServiceNameModel, ServiceCategoryModel
from models.database import get_session
from services.service_service import ServiceNameService, ServiceCategoryService

router_service = APIRouter()
ROUTE_SERVICE = '/service/'
ROUTE_CATEGORY = '/category/'
ROUTE_SERVICE_CATEGORY = f'{ROUTE_SERVICE}{ROUTE_CATEGORY[1:]}'


@router_service.get(ROUTE_CATEGORY + '{pk}/', response_model=ServiceCategoryModel)
async def view_get_service_category_by_id(pk: int, session: AsyncSession = Depends(get_session)):
    category = await ServiceCategoryService(db_session=session).get(pk=pk)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return category


@router_service.get(ROUTE_CATEGORY, response_model=list[ServiceCategoryModel])
async def view_get_service_category_all(session: AsyncSession = Depends(get_session)):
    return await ServiceCategoryService(db_session=session).get_all()


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
