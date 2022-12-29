from sqlalchemy import select
from models import ClientModel
from models.user_model import Gender
from services.base_service import BaseService


class ClientService(BaseService):
    def add(self, employee: ClientModel):
        new_city = ClientModel(
            phone=employee.phone,
            email=employee.email,
            last_name=employee.last_name,
            first_name=employee.first_name,
            birth_date=employee.birth_date,
            gender=Gender.MALE,
        )
        self.db_session.add(new_city)
        return new_city

    async def get_all(self) -> list[ClientModel]:
        result = await self.db_session.execute(
            select(ClientModel).order_by(ClientModel.last_name.desc()).limit(20)
        )
        return result.scalars().all()
