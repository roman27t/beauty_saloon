from sqlalchemy import select

from models import ClientModel
from schemas.user_schemas import ClientInSchema
from services.base_service import BaseService


# todo duplicate
class ClientService(BaseService):
    def add(self, schema: ClientInSchema):
        client_schema = ClientModel(**schema.dict())
        self.db_session.add(client_schema)
        return client_schema
    
    def update(self, employee_db: ClientModel, schema: ClientInSchema):
        for key, value in schema.dict(exclude_unset=True).items():
            setattr(employee_db, key, value)
        self.db_session.add(employee_db)

    async def get_all(self) -> list[ClientModel]:
        result = await self.db_session.execute(select(ClientModel).order_by(ClientModel.last_name.desc()).limit(20))
        return result.scalars().all()
    
    async def get(self, pk: int) -> ClientModel:
        result = await self.db_session.get(ClientModel, pk)
        return result
