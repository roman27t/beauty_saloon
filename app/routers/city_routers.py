from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import DuplicatedEntryError
from models.database import get_session
from models import EmployeeModel
from services.city_service import EmployeeService

router = APIRouter()


@router.get('/items/{item_id}')
def read_item(item_id: int, q: Union[str, None] = None):
    return {'item_id': item_id, 'q': q}


@router.get('/employee/', response_model=list[EmployeeModel], status_code=201)
async def get_client(session: AsyncSession = Depends(get_session)):
    cities = await EmployeeService(db_session=session).get_biggest_cities()
    return cities  # [CitySchema(name=c.name, population=c.population) for c in cities]


@router.post('/employee/')
async def add_client(employee: EmployeeModel, session: AsyncSession = Depends(get_session)):
    city = EmployeeService(db_session=session).add_city(employee=employee)
    try:
        await session.commit()
        return city
    except IntegrityError:
        await session.rollback()
        raise DuplicatedEntryError('The city is already stored')
