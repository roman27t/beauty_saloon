from typing import Type

from models import CategoryModel, ServiceNameModel
from services.base_service import AbstractService


class CategoryService(AbstractService):
    @property
    def _table(self) -> Type[CategoryModel]:
        return CategoryModel


class ServiceNameService(AbstractService):
    @property
    def _table(self) -> Type[ServiceNameModel]:
        return ServiceNameModel
