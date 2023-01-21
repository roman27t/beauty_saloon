from typing import Type

from models import ClientModel
from services import ServiceRegistry
from services.base_service import AbstractService


class ClientService(AbstractService):
    @property
    def _table(self) -> Type[ClientModel]:
        return ClientModel


ServiceRegistry.register(model=ClientModel, service_class=ClientService)
