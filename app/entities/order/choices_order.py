import enum
from enum import Enum

from entities.users.models_user import ClientModel, EmployeeModel


class OrderFilter(str, Enum):
    employee = 'employee'
    client = 'client'

    def get_model(self):
        return EmployeeModel if self.value == self.employee else ClientModel

    def invert(self) -> str:
        return self.client if self.value == self.employee else self.employee

    def _build_id(self, name: str) -> str:
        return f'{name}_id'

    @property
    def get_value_id(self) -> str:
        return self._build_id(name=self.value)

    @property
    def get_value_invert_id(self) -> str:
        return self._build_id(name=self.invert())


class StatusOrder(str, enum.Enum):
    WAIT = 'W'
    CANCEL = 'C'
    PAID = 'PN'
    SUCCESS = 'P'
    PROC_RETURN = 'CR'
    RETURN = 'R'
