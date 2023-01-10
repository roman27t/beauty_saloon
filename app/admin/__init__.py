from .order_admin import OrderAdmin
from .user_admin import ClientAdmin, EmployeeAdmin
from .offer_admin import OfferLinkAdmin
from .service_admin import ServiceNameAdmin, ServiceCategoryAdmin

admin_classes = (
    EmployeeAdmin,
    ClientAdmin,
    ServiceCategoryAdmin,
    ServiceNameAdmin,
    OfferLinkAdmin,
    OrderAdmin,
)
