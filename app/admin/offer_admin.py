from sqladmin import ModelView

from entities.offer.offer_model import OfferLinkModel


class OfferLinkAdmin(ModelView, model=OfferLinkModel):
    column_list = [
        OfferLinkModel.id,
        OfferLinkModel.created_at,
        OfferLinkModel.changed_at,
        OfferLinkModel.is_active,
        OfferLinkModel.employee_id,
        OfferLinkModel.service_name_id,
        OfferLinkModel.rate,
    ]
    column_details_exclude_list = [OfferLinkModel.employee, OfferLinkModel.service_name]
