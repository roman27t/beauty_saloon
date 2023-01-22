from typing import Type

from services.base_service import AbstractService
from entities.service_name.models_service_name import ServiceNameModel


class ServiceNameService(AbstractService):
    @property
    def _table(self) -> Type[ServiceNameModel]:
        return ServiceNameModel
