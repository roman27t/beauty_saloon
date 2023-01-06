from sqladmin import ModelView

from models import CategoryModel, ServiceNameModel


class ServiceCategoryAdmin(ModelView, model=CategoryModel):
    column_list = [CategoryModel.id, CategoryModel.name, CategoryModel.detail]


class ServiceNameAdmin(ModelView, model=ServiceNameModel):
    column_list = [ServiceNameModel.id, ServiceNameModel.name, ServiceNameModel.detail]
