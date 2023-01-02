from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models import EmployeeModel
from models.database import get_session
from models.user_model import EmployeeInOptionalSchema
from services.employee_service import EmployeeService


async def valid_patch_id(pk: int, session: AsyncSession = Depends(get_session)) -> EmployeeModel:
    user = await EmployeeService(db_session=session).get(pk=pk)
    if not user:
        raise HTTPException(status_code=404, detail=f'item with id {pk} not found')
    return user


async def valid_patch_schema(schema: EmployeeInOptionalSchema) -> EmployeeInOptionalSchema:
    if not schema.dict(exclude_unset=True):
        raise HTTPException(status_code=400, detail='empty data')
    return schema
