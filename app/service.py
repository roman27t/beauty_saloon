from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import CityModel


def add_city(session: AsyncSession, name: str, population: int):
    new_city = CityModel(name=name, population=population)
    session.add(new_city)
    return new_city


async def get_biggest_cities(session: AsyncSession) -> list[CityModel]:
    result = await session.execute(
        select(CityModel).order_by(CityModel.population.desc()).limit(20)
    )
    return result.scalars().all()
