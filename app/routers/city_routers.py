from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import DuplicatedEntryError
from models.database import get_session
from models import CityModel
from services.city_service import CityService

router = APIRouter()


@router.get('/items/{item_id}')
def read_item(item_id: int, q: Union[str, None] = None):
    return {'item_id': item_id, 'q': q}


@router.get('/cities/biggest', response_model=list[CityModel], status_code=201)
async def get_biggest_cities_view(session: AsyncSession = Depends(get_session)):
    cities = await CityService(db_session=session).get_biggest_cities()
    return cities  # [CitySchema(name=c.name, population=c.population) for c in cities]


@router.post('/cities/')
async def add_city_view(city: CityModel, session: AsyncSession = Depends(get_session)):
    city = CityService(db_session=session).add_city(name=city.name, population=city.population)
    try:
        await session.commit()
        return city
    except IntegrityError:
        await session.rollback()
        raise DuplicatedEntryError('The city is already stored')
