from typing import Type

from services.base_service import AbstractService
from entities.users.models_user import ClientModel


class ClientService(AbstractService):
    @property
    def _table(self) -> Type[ClientModel]:
        return ClientModel
