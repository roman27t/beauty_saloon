from entities.category.admins_category import CategoryAdmin
from entities.offer.admins_offer import OfferLinkAdmin
from entities.order.order_admin import OrderAdmin, OrderDetailAdmin
from entities.service_name.admins_service_name import ServiceNameAdmin
from entities.users.admins_user import EmployeeAdmin, ClientAdmin

admin_classes = (
    CategoryAdmin,
    EmployeeAdmin,
    ClientAdmin,
    ServiceNameAdmin,
    OfferLinkAdmin,
    OrderAdmin,
    OrderDetailAdmin,
)
