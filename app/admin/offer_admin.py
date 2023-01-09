from sqladmin import ModelView

from models import OfferLinkModel


class OfferLinkAdmin(ModelView, model=OfferLinkModel):
    column_list = [
        OfferLinkModel.id,
        OfferLinkModel.employee_id,
        OfferLinkModel.service_name_id,
        OfferLinkModel.rate,
    ]
    column_details_exclude_list = [OfferLinkModel.employee, OfferLinkModel.service_name]
