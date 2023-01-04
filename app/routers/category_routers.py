from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import ServiceCategoryModel
from models.database import get_session
from services.service_service import ServiceCategoryService

router_category = APIRouter()
ROUTE_CATEGORY = '/category/'


@router_category.get(ROUTE_CATEGORY + '{pk}/', response_model=ServiceCategoryModel)
async def view_get_service_category_by_id(pk: int, session: AsyncSession = Depends(get_session)):
    category = await ServiceCategoryService(db_session=session).get(pk=pk)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return category


@router_category.get(ROUTE_CATEGORY, response_model=list[ServiceCategoryModel])
async def view_get_service_category_all(session: AsyncSession = Depends(get_session)):
    return await ServiceCategoryService(db_session=session).get_all()
