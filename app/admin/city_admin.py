from sqladmin import ModelView
from models import EmployeeModel, ClientModel


class EmployeeAdmin(ModelView, model=EmployeeModel):
    column_list = [EmployeeModel.id, EmployeeModel.last_name]


class ClientAdmin(ModelView, model=ClientModel):
    column_list = [ClientModel.id, ClientModel.last_name]
