from enum import Enum

from entities.users.model_user import ClientModel, EmployeeModel


class OrderFilter(str, Enum):
    employee = 'employee'
    client = 'client'

    def get_model(self):
        return EmployeeModel if self.value == self.employee else ClientModel

    def invert(self) -> str:
        return self.client if self.value == self.employee else self.employee
