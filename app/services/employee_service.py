from typing import Type

from entities.users.model_user import EmployeeModel
from services.base_service import AbstractService


class EmployeeService(AbstractService):
    @property
    def _table(self) -> Type[EmployeeModel]:
        return EmployeeModel
