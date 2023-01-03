from typing import Type

from models import ClientModel
from services.base_service import AbstractService


class ClientService(AbstractService):
    @property
    def _table(self) -> Type[ClientModel]:
        return ClientModel
