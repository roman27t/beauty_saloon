from typing import Type

from entities.users.models_user import ClientModel
from tests.abstract_user import UserAbstract
from schemas.user_schemas import ClientInSchema, ClientInOptionalSchema
from services.stub_init_service import LAST_NAMES


class TestClient(UserAbstract):
    @property
    def _url_path(self) -> str:
        return 'client'

    @property
    def _model(self) -> Type[ClientModel]:
        return ClientModel

    @property
    def _in_schema(self) -> Type[ClientInSchema]:
        return ClientInSchema

    @property
    def _in_optional_schema(self) -> Type[ClientInOptionalSchema]:
        return ClientInOptionalSchema

    @property
    def _last_name(self) -> str:
        return LAST_NAMES[5]
