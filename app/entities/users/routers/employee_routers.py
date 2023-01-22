from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import ValidGetByIdDependency, valid_empty_schema
from routers.consts import RouteSlug
from models.database import get_session
from entities.users.models_user import EmployeeModel
from entities.users.schemas_users import (
    EmployeeInSchema,
    EmployeeInOptionalSchema,
)
from entities.users.services.employee_service import EmployeeService

router_employee = APIRouter()
ROUTE_EMPLOYEE = '/employee/'


@router_employee.get(ROUTE_EMPLOYEE + RouteSlug.pk, response_model=EmployeeModel)
async def view_get_employee_by_id(pk: int, session: AsyncSession = Depends(get_session)):
    return await EmployeeService(db_session=session).get(pk=pk)


@router_employee.get(ROUTE_EMPLOYEE, response_model=list[EmployeeModel])
async def view_get_employee_all(session: AsyncSession = Depends(get_session)):
    return await EmployeeService(db_session=session).get_all()


@router_employee.post(ROUTE_EMPLOYEE)
async def view_add_employee(employee: EmployeeInSchema, session: AsyncSession = Depends(get_session)):
    return await EmployeeService(db_session=session).add(schema=employee)


@router_employee.patch(ROUTE_EMPLOYEE + RouteSlug.pk, response_model=EmployeeModel)
async def view_patch_employee(
    schema: EmployeeInOptionalSchema = Depends(valid_empty_schema(class_schema=EmployeeInOptionalSchema)),
    employee_db: EmployeeModel = Depends(ValidGetByIdDependency(class_service=EmployeeService)),
    session: AsyncSession = Depends(get_session),
):
    await EmployeeService(db_session=session).update(obj_db=employee_db, schema=schema)
    return employee_db
