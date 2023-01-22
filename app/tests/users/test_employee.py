from typing import Type

from entities.users.models_user import EmployeeModel
from tests.users.abstract_user import UserAbstract
from entities.users.schemas_users import EmployeeInSchema, EmployeeInOptionalSchema
from services.stub_init_service import LAST_NAMES


class TestEmployee(UserAbstract):
    @property
    def _url_path(self) -> str:
        return 'employee'

    @property
    def _model(self) -> Type[EmployeeModel]:
        return EmployeeModel

    @property
    def _in_schema(self) -> Type[EmployeeInSchema]:
        return EmployeeInSchema

    @property
    def _in_optional_schema(self) -> Type[EmployeeInOptionalSchema]:
        return EmployeeInOptionalSchema

    @property
    def _last_name(self) -> str:
        return LAST_NAMES[0]
