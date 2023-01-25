from entities.users.admins_user import ClientAdmin, EmployeeAdmin
from entities.offer.admins_offer import OfferAdmin
from entities.order.admins_order import OrderAdmin, OrderDetailAdmin
from entities.category.admins_category import CategoryAdmin
from entities.service_name.admins_service_name import ServiceNameAdmin

admin_classes = (
    CategoryAdmin,
    EmployeeAdmin,
    ClientAdmin,
    ServiceNameAdmin,
    OfferAdmin,
    OrderAdmin,
    OrderDetailAdmin,
)
