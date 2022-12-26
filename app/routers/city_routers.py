from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import DuplicatedEntryError
from database import get_session
from models import CityModel
from service import get_biggest_cities, add_city

router = APIRouter()


@router.get('/items/{item_id}')
def read_item(item_id: int, q: Union[str, None] = None):
    return {'item_id': item_id, 'q': q}


@router.get('/cities/biggest', response_model=list[CityModel], status_code=201)
async def get_biggest_cities_view(session: AsyncSession = Depends(get_session)):
    cities = await get_biggest_cities(session)
    return cities  # [CitySchema(name=c.name, population=c.population) for c in cities]


@router.post('/cities/')
async def add_city_view(city: CityModel, session: AsyncSession = Depends(get_session)):
    city = add_city(session, city.name, city.population)
    try:
        await session.commit()
        return city
    except IntegrityError:
        await session.rollback()
        raise DuplicatedEntryError('The city is already stored')
