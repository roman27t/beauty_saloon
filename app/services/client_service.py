from typing import Type

from entities.users.model_user import ClientModel
from services.base_service import AbstractService


class ClientService(AbstractService):
    @property
    def _table(self) -> Type[ClientModel]:
        return ClientModel
