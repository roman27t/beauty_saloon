from .user_admin import ClientAdmin, EmployeeAdmin
from .offer_admin import OfferLinkAdmin
from .order_admin import OrderAdmin, OrderDetailAdmin
from .service_admin import ServiceNameAdmin

admin_classes = (
    EmployeeAdmin,
    ClientAdmin,
    ServiceNameAdmin,
    OfferLinkAdmin,
    OrderAdmin,
    OrderDetailAdmin,
)
