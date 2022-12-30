from sqlalchemy import select

from models import ClientModel
from models.user_model import Gender
from services.base_service import BaseService


class ClientService(BaseService):
    def add(self, schema: ClientModel):
        client_schema = ClientModel(
            phone=schema.phone,
            email=schema.email,
            last_name=schema.last_name,
            first_name=schema.first_name,
            birth_date=schema.birth_date,
            gender=Gender.MALE,
        )
        self.db_session.add(client_schema)
        return client_schema

    async def get_all(self) -> list[ClientModel]:
        result = await self.db_session.execute(select(ClientModel).order_by(ClientModel.last_name.desc()).limit(20))
        return result.scalars().all()
