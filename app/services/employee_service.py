from sqlalchemy import select

from models import EmployeeModel
from models.user_model import Gender, EmployeeInSchema
from services.base_service import BaseService


class EmployeeService(BaseService):
    def add(self, employee: EmployeeInSchema):
        employee_schema = EmployeeModel(
            phone=employee.phone,
            email=employee.email,
            last_name=employee.last_name,
            first_name=employee.first_name,
            birth_date=employee.birth_date,
            gender=Gender.MALE,
        )
        self.db_session.add(employee_schema)
        return employee_schema

    async def get_all(self) -> list[EmployeeModel]:
        result = await self.db_session.execute(select(EmployeeModel).order_by(EmployeeModel.last_name.desc()).limit(20))
        return result.scalars().all()

    async def get(self, pk: int) -> EmployeeModel:
        result = await self.db_session.get(EmployeeModel, pk)
        return result
