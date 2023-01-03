from typing import Type

from models import ServiceNameModel, ServiceCategoryModel
from services.base_service import AbstractService


class ServiceCategoryService(AbstractService):
    @property
    def _table(self) -> Type[ServiceCategoryModel]:
        return ServiceCategoryModel


class ServiceNameService(AbstractService):
    @property
    def _table(self) -> Type[ServiceNameModel]:
        return ServiceNameModel
