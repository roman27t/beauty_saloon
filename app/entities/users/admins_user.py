from sqladmin import ModelView

from entities.users.models_user import ClientModel, EmployeeModel


class EmployeeAdmin(ModelView, model=EmployeeModel):
    column_list = [
        EmployeeModel.id,
        EmployeeModel.created_at,
        EmployeeModel.changed_at,
        EmployeeModel.is_active,
        EmployeeModel.last_name,
        EmployeeModel.first_name,
        EmployeeModel.birth_date,
    ]
    column_searchable_list = [EmployeeModel.last_name]


class ClientAdmin(ModelView, model=ClientModel):
    column_list = [
        ClientModel.id,
        ClientModel.created_at,
        ClientModel.changed_at,
        ClientModel.is_active,
        ClientModel.last_name,
        ClientModel.first_name,
        ClientModel.birth_date,
    ]
    column_searchable_list = [ClientModel.last_name]
