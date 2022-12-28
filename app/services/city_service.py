import datetime as dt
from sqlalchemy import select
from models import EmployeeModel
from services.base_service import BaseService


# class CityService(BaseService):
#     def add_city(self, name: str, population: int):
#         new_city = CityModel(name=name, population=population)
#         self.db_session.add(new_city)
#         return new_city
#
#     async def get_biggest_cities(self) -> list[CityModel]:
#         result = await self.db_session.execute(
#             select(CityModel).order_by(CityModel.population.desc()).limit(20)
#         )
#         return result.scalars().all()


class EmployeeService(BaseService):
    def add_city(self, employee: EmployeeModel):
        new_city = EmployeeModel(
            phone=employee.phone,
            email=employee.email,
            last_name=employee.last_name,
            first_name=employee.first_name,
            birthday=employee.birthday,
        )
        self.db_session.add(new_city)
        return new_city

    async def get_biggest_cities(self) -> list[EmployeeModel]:
        result = await self.db_session.execute(
            select(EmployeeModel).order_by(EmployeeModel.last_name.desc()).limit(20)
        )
        return result.scalars().all()