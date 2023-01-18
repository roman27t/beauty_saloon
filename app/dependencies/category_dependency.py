from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import CategoryModel
from models.database import get_session
from schemas.category_schema import CategoryOptionalSchema
from services.service_service import CategoryService


async def valid_patch_id(pk: int, session: AsyncSession = Depends(get_session)) -> CategoryModel:
    return await CategoryService(db_session=session).get(pk=pk)


async def valid_patch_schema(schema: CategoryOptionalSchema) -> CategoryOptionalSchema:
    if not schema.dict(exclude_unset=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='empty data')
    return schema
