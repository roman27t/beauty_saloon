from sqlalchemy import select
from models import CityModel
from services.base_service import BaseService


class CityService(BaseService):
    def add_city(self, name: str, population: int):
        new_city = CityModel(name=name, population=population)
        self.db_session.add(new_city)
        return new_city

    async def get_biggest_cities(self) -> list[CityModel]:
        result = await self.db_session.execute(
            select(CityModel).order_by(CityModel.population.desc()).limit(20)
        )
        return result.scalars().all()
