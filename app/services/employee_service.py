from sqlalchemy import select

from models import EmployeeModel
from models.user_model import Gender
from services.base_service import BaseService


class EmployeeService(BaseService):
    def add(self, employee: EmployeeModel):
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
