from typing import Type

from services.base_service import AbstractService
from entities.category.models_category import CategoryModel


class CategoryService(AbstractService):
    @property
    def _table(self) -> Type[CategoryModel]:
        return CategoryModel
