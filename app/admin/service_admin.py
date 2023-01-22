from sqladmin import ModelView

from models import ServiceNameModel


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
