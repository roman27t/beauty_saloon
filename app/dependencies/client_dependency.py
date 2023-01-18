from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import ClientModel
from models.database import get_session
from schemas.user_schemas import EmployeeInOptionalSchema
from services.client_service import ClientService


async def valid_patch_id(pk: int, session: AsyncSession = Depends(get_session)) -> ClientModel:
    return await ClientService(db_session=session).get(pk=pk)


async def valid_patch_schema(schema: EmployeeInOptionalSchema) -> EmployeeInOptionalSchema:
    if not schema.dict(exclude_unset=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='empty data')
    return schema
