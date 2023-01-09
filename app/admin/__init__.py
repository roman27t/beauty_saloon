from .offer_admin import OfferLinkAdmin
from .user_admin import ClientAdmin, EmployeeAdmin
from .service_admin import ServiceNameAdmin, ServiceCategoryAdmin

admin_classes = (
    EmployeeAdmin,
    ClientAdmin,
    ServiceCategoryAdmin,
    ServiceNameAdmin,
    OfferLinkAdmin,
)
