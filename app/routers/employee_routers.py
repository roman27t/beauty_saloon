from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import EmployeeModel
from models.database import get_session
from schemas.user_schemas import EmployeeInSchema, EmployeeInOptionalSchema
from services.employee_service import EmployeeService
from dependencies.employee_dependency import valid_patch_id, valid_patch_schema

router_employee = APIRouter()
ROUTE_EMPLOYEE = '/employee/'


@router_employee.get(ROUTE_EMPLOYEE + '{pk}/', response_model=EmployeeModel)
async def view_get_employee_by_id(pk: int, session: AsyncSession = Depends(get_session)):
    user = await EmployeeService(db_session=session).get(pk=pk)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return user


@router_employee.get(ROUTE_EMPLOYEE, response_model=list[EmployeeModel])
async def view_get_employee_all(session: AsyncSession = Depends(get_session)):
    return await EmployeeService(db_session=session).get_all()


@router_employee.post(ROUTE_EMPLOYEE)
async def view_add_employee(employee: EmployeeInSchema, session: AsyncSession = Depends(get_session)):
    employee_schema = await EmployeeService(db_session=session).add(schema=employee)
    return employee_schema


@router_employee.patch(ROUTE_EMPLOYEE + '{pk}/', response_model=EmployeeModel)
async def view_patch_employee(
    schema: EmployeeInOptionalSchema = Depends(valid_patch_schema),
    employee_db: EmployeeModel = Depends(valid_patch_id),
    session: AsyncSession = Depends(get_session),
):
    await EmployeeService(db_session=session).update(obj_db=employee_db, schema=schema)
    return employee_db
