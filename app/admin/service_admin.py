from sqladmin import ModelView

from models import ServiceCategoryModel


class ServiceCategoryAdmin(ModelView, model=ServiceCategoryModel):
    column_list = [ServiceCategoryModel.id, ServiceCategoryModel.name, ServiceCategoryModel.detail]
