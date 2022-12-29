from sqlalchemy import select
from models import EmployeeModel
from services.base_service import BaseService


class EmployeeService(BaseService):
    def add(self, employee: EmployeeModel):
        new_city = EmployeeModel(
            phone=employee.phone,
            email=employee.email,
            last_name=employee.last_name,
            first_name=employee.first_name,
            birthday=employee.birthday,
        )
        self.db_session.add(new_city)
        return new_city

    async def get_all(self) -> list[EmployeeModel]:
        result = await self.db_session.execute(
            select(EmployeeModel).order_by(EmployeeModel.last_name.desc()).limit(20)
        )
        return result.scalars().all()
