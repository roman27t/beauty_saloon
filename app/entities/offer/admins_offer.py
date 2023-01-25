from sqladmin import ModelView

from entities.offer.models_offer import OfferModel


class OfferLinkAdmin(ModelView, model=OfferModel):
    column_list = [
        OfferModel.id,
        OfferModel.created_at,
        OfferModel.changed_at,
        OfferModel.is_active,
        OfferModel.employee_id,
        OfferModel.service_name_id,
        OfferModel.rate,
    ]
    column_details_exclude_list = [OfferModel.employee, OfferModel.service_name]
