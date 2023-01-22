from sqladmin import ModelView

from entities.category.models_category import CategoryModel


class CategoryAdmin(ModelView, model=CategoryModel):
    column_list = [
        CategoryModel.id,
        CategoryModel.created_at,
        CategoryModel.changed_at,
        CategoryModel.name,
        CategoryModel.is_active,
    ]
    column_searchable_list = [CategoryModel.name]
    column_details_exclude_list = [CategoryModel.services]
