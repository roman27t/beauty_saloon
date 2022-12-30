from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import DuplicatedEntryError
from models.database import get_session
from models import EmployeeModel
from services.employee_service import EmployeeService

router = APIRouter()
_route = '/employee/'


@router.get('/items/{item_id}')
def read_item(item_id: int, q: Union[str, None] = None):
    return {'item_id': item_id, 'q': q}


@router.get(_route, response_model=list[EmployeeModel], status_code=201)
async def get_all_employee(session: AsyncSession = Depends(get_session)):
    users = await EmployeeService(db_session=session).get_all()
    return users  # [CitySchema(name=c.name, population=c.population) for c in cities]


@router.post(_route)
async def add_employee(employee: EmployeeModel, session: AsyncSession = Depends(get_session)):
    employee_schema = EmployeeService(db_session=session).add(employee=employee)
    try:
        await session.commit()
        return employee_schema
    except IntegrityError:
        await session.rollback()
        raise DuplicatedEntryError('The employee is already stored')
