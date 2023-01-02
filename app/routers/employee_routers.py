from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import EmployeeModel
from core.exceptions import DuplicatedEntryError
from models.database import get_session
from models.user_model import EmployeeInSchema, EmployeeInOptionalSchema
from services.employee_service import EmployeeService

router = APIRouter()
ROUTE_EMPLOYEE = '/employee/'


@router.get(ROUTE_EMPLOYEE + '{pk}/', response_model=EmployeeModel, status_code=200)
async def get_employee_by_id(pk: int, session: AsyncSession = Depends(get_session)):
    user = await EmployeeService(db_session=session).get(pk=pk)
    if not user:
        raise HTTPException(status_code=404, detail=f'item with id {pk} not found')
    return user


@router.get(ROUTE_EMPLOYEE, response_model=list[EmployeeModel], status_code=200)
async def get_employee_all(session: AsyncSession = Depends(get_session)):
    users = await EmployeeService(db_session=session).get_all()
    return users  # [CitySchema(name=c.name, population=c.population) for c in cities]


@router.post(ROUTE_EMPLOYEE)
async def add_employee(employee: EmployeeInSchema, session: AsyncSession = Depends(get_session)):
    employee_schema = EmployeeService(db_session=session).add(schema=employee)
    try:
        await session.commit()
        return employee_schema
    except IntegrityError:
        await session.rollback()
        raise DuplicatedEntryError('The employee is already stored')


async def valid_post_id(pk: int, session: AsyncSession = Depends(get_session)) -> EmployeeModel:
    user = await EmployeeService(db_session=session).get(pk=pk)
    if not user:
        raise HTTPException(status_code=404, detail=f'item with id {pk} not found')
    return user


async def valid_schema(schema: EmployeeInOptionalSchema) -> EmployeeInOptionalSchema:
    if not schema.dict(exclude_unset=True):
        raise HTTPException(status_code=400, detail='empty data')
    return schema


@router.patch(ROUTE_EMPLOYEE + '{pk}/', response_model=EmployeeModel)
async def patch_employee(
    schema: EmployeeInOptionalSchema=Depends(valid_schema),
    employee_db: EmployeeModel=Depends(valid_post_id),
    session: AsyncSession = Depends(get_session),
):
    EmployeeService(db_session=session).update(employee_db=employee_db, schema=schema)
    await session.commit()
    await session.refresh(employee_db)
    return employee_db
