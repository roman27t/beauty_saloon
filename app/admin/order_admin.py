from sqladmin import ModelView

from models import OrderModel


class OrderAdmin(ModelView, model=OrderModel):
    column_list = [
        OrderModel.id,
        OrderModel.created_at,
        OrderModel.changed_at,
        OrderModel.start_at,
        OrderModel.end_at,
        OrderModel.employee_id,
        OrderModel.client_id,
    ]
    column_details_exclude_list = [OrderModel.employee, OrderModel.client]
