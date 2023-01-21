from typing import Type

from models import EmployeeModel
from services import ServiceRegistry
from services.base_service import AbstractService


class EmployeeService(AbstractService):
    @property
    def _table(self) -> Type[EmployeeModel]:
        return EmployeeModel


ServiceRegistry.register(model=EmployeeModel, service_class=EmployeeService)
