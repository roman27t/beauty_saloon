from sqladmin import ModelView

from models import ServiceNameModel, ServiceCategoryModel


class ServiceCategoryAdmin(ModelView, model=ServiceCategoryModel):
    column_list = [ServiceCategoryModel.id, ServiceCategoryModel.name, ServiceCategoryModel.detail]


class ServiceNameAdmin(ModelView, model=ServiceNameModel):
    column_list = [ServiceNameModel.id, ServiceNameModel.name, ServiceNameModel.detail]
