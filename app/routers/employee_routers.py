from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.user_dependency import valid_patch_id, valid_patch_schema
from models import EmployeeModel
from core.exceptions import DuplicatedEntryError
from models.database import get_session
from schemas.user_schemas import EmployeeInSchema, EmployeeInOptionalSchema
from services.employee_service import EmployeeService

router = APIRouter()
ROUTE_EMPLOYEE = '/employee/'


@router.get(ROUTE_EMPLOYEE + '{pk}/', response_model=EmployeeModel)
async def view_get_employee_by_id(pk: int, session: AsyncSession = Depends(get_session)):
    user = await EmployeeService(db_session=session).get(pk=pk)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return user


@router.get(ROUTE_EMPLOYEE, response_model=list[EmployeeModel])
async def view_get_employee_all(session: AsyncSession = Depends(get_session)):
    return await EmployeeService(db_session=session).get_all()


@router.post(ROUTE_EMPLOYEE)
async def view_add_employee(employee: EmployeeInSchema, session: AsyncSession = Depends(get_session)):
    employee_schema = EmployeeService(db_session=session).add(schema=employee)
    try:
        await session.commit()
        return employee_schema
    except IntegrityError:
        await session.rollback()
        raise DuplicatedEntryError('The employee is already stored')


@router.patch(ROUTE_EMPLOYEE + '{pk}/', response_model=EmployeeModel)
async def view_patch_employee(
    schema: EmployeeInOptionalSchema=Depends(valid_patch_schema),
    employee_db: EmployeeModel=Depends(valid_patch_id),
    session: AsyncSession = Depends(get_session),
):
    EmployeeService(db_session=session).update(obj_db=employee_db, schema=schema)
    await session.commit()
    await session.refresh(employee_db)
    return employee_db
