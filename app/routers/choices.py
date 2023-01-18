from enum import Enum

from models import EmployeeModel, ClientModel


class OrderFilter(str, Enum):
    employee = 'employee'
    client = 'client'

    def get_model(self):
        return EmployeeModel if self.value == self.employee else ClientModel

    def invert(self) -> str:
        return self.client if self.value == self.employee else self.employee


