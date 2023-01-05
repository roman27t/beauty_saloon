from fastapi import Depends, HTTPException, status
from services.service_service import ServiceCategoryService
from sqlalchemy.ext.asyncio import AsyncSession

from models import ServiceCategoryModel
from models.database import get_session
from schemas.category_schema import CategoryOptionalSchema


async def valid_patch_id(pk: int, session: AsyncSession = Depends(get_session)) -> ServiceCategoryModel:
    category = await ServiceCategoryService(db_session=session).get(pk=pk)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return category


async def valid_patch_schema(schema: CategoryOptionalSchema) -> CategoryOptionalSchema:
    if not schema.dict(exclude_unset=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='empty data')
    return schema
