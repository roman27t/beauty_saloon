from typing import Type

from category.model_category import CategoryModel
from services.base_service import AbstractService


class CategoryService(AbstractService):
    @property
    def _table(self) -> Type[CategoryModel]:
        return CategoryModel
