from fastapi import Depends, HTTPException, status

from schemas.service_name_schema import ServiceNameOptionalSchema
from services.service_service import ServiceNameService
from sqlalchemy.ext.asyncio import AsyncSession

from models import CategoryModel
from models.database import get_session


async def valid_patch_id(pk: int, session: AsyncSession = Depends(get_session)) -> CategoryModel:
    service = await ServiceNameService(db_session=session).get(pk=pk)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return service


async def valid_patch_schema(schema: ServiceNameOptionalSchema) -> ServiceNameOptionalSchema:
    if not schema.dict(exclude_unset=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='empty data')
    return schema
