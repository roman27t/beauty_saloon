from typing import Type

from entities.service_name.models_service_name import ServiceNameModel
from services.base_service import AbstractService


class ServiceNameService(AbstractService):
    @property
    def _table(self) -> Type[ServiceNameModel]:
        return ServiceNameModel