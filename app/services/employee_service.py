from sqlalchemy import select

from models import EmployeeModel
from schemas.user_schemas import EmployeeInSchema
from services.base_service import BaseService


class EmployeeService(BaseService):
    def add(self, schema: EmployeeInSchema):
        employee_db = EmployeeModel(**schema.dict())
        self.db_session.add(employee_db)
        return employee_db

    def update(self, employee_db: EmployeeModel, schema: EmployeeInSchema):
        for key, value in schema.dict(exclude_unset=True).items():
            setattr(employee_db, key, value)
        self.db_session.add(employee_db)

    async def get_all(self) -> list[EmployeeModel]:
        result = await self.db_session.execute(select(EmployeeModel).order_by(EmployeeModel.last_name.desc()).limit(20))
        return result.scalars().all()

    async def get(self, pk: int) -> EmployeeModel:
        result = await self.db_session.get(EmployeeModel, pk)
        return result
