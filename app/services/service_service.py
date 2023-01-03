from typing import Type

from models import ServiceCategoryModel
from services.base_service import AbstractService


class ServiceCategoryService(AbstractService):
    @property
    def _table(self) -> Type[ServiceCategoryModel]:
        return ServiceCategoryModel
