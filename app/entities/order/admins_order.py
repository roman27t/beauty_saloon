from sqladmin import ModelView

from entities.order.models_order import OrderModel, OrderDetailModel


class OrderAdmin(ModelView, model=OrderModel):
    column_list = [
        OrderModel.id,
        OrderModel.created_at,
        OrderModel.changed_at,
        OrderModel.start_at,
        OrderModel.end_at,
        OrderModel.employee_id,
        OrderModel.client_id,
        OrderModel.price,
    ]
    column_details_exclude_list = [OrderModel.employee, OrderModel.client, OrderModel.service, OrderModel.order_detail]


class OrderDetailAdmin(ModelView, model=OrderDetailModel):
    column_list = [
        OrderDetailModel.id,
        OrderDetailModel.created_at,
        OrderDetailModel.changed_at,
        OrderDetailModel.name,
    ]
    column_details_exclude_list = [OrderDetailModel.order]
