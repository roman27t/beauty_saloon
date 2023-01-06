from sqladmin import ModelView

from models import CategoryModel, ServiceNameModel


class ServiceCategoryAdmin(ModelView, model=CategoryModel):
    column_list = [
        CategoryModel.id,
        CategoryModel.created_at,
        CategoryModel.changed_at,
        CategoryModel.name,
        CategoryModel.is_active,
    ]
    column_searchable_list = [CategoryModel.name]
    column_details_exclude_list = [CategoryModel.services]


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
    column_details_exclude_list = [ServiceNameModel.category]
