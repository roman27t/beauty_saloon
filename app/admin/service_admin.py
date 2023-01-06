from sqladmin import ModelView

from models import CategoryModel, ServiceNameModel


class ServiceCategoryAdmin(ModelView, model=CategoryModel):
    column_list = [
        CategoryModel.id,
        CategoryModel.created_at,
        CategoryModel.changed_at,
        CategoryModel.name,
        CategoryModel.detail,
    ]
    column_searchable_list = [CategoryModel.name]


class ServiceNameAdmin(ModelView, model=ServiceNameModel):
    column_list = [
        ServiceNameModel.id,
        ServiceNameModel.created_at,
        ServiceNameModel.changed_at,
        ServiceNameModel.name,
        ServiceNameModel.is_active,
        ServiceNameModel.price,
    ]
    column_searchable_list = [ServiceNameModel.name]
