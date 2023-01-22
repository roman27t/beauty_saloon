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


class StatusOrder(str, enum.Enum):
    WAIT = 'W'
    CANCEL = 'C'
    PAID = 'PN'
    SUCCESS = 'P'
    PROC_RETURN = 'CR'
    RETURN = 'R'
