from sqladmin import ModelView

from models import OrderModel, OrderDetailModel


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
    column_details_exclude_list = [OrderModel.employee, OrderModel.client, OrderModel.service, OrderModel.order_detail]



class OrderDetailAdmin(ModelView, model=OrderDetailModel):
    column_list = [
        OrderDetailModel.id,
        OrderDetailModel.created_at,
        OrderDetailModel.changed_at,
        OrderDetailModel.name,
        OrderDetailModel.price,
    ]
    column_details_exclude_list = [OrderDetailModel.order]