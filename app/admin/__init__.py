from .offer_admin import OfferLinkAdmin
from .order_admin import OrderAdmin, OrderDetailAdmin
from .service_admin import ServiceNameAdmin

admin_classes = (
    ServiceNameAdmin,
    OfferLinkAdmin,
    OrderAdmin,
    OrderDetailAdmin,
)
