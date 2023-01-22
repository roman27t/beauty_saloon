from typing import Type

from services.base_service import AbstractService
from entities.users.models_user import EmployeeModel


class EmployeeService(AbstractService):
    @property
    def _table(self) -> Type[EmployeeModel]:
        return EmployeeModel
