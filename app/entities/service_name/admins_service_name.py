from sqladmin import ModelView

from entities.service_name.models_service_name import ServiceNameModel


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
