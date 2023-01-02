from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import ClientModel
from models.database import get_session
from models.user_model import EmployeeInOptionalSchema
from services.client_service import ClientService


# todo common ?
async def valid_patch_id(pk: int, session: AsyncSession = Depends(get_session)) -> ClientModel:
    user = await ClientService(db_session=session).get(pk=pk)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return user


async def valid_patch_schema(schema: EmployeeInOptionalSchema) -> EmployeeInOptionalSchema:
    if not schema.dict(exclude_unset=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='empty data')
    return schema
