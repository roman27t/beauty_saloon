from config import i_config
from routers.index import router_index
from routers.stub_init_routers import router_init_stub
from entities.offer.routers_offer import router_offer
from entities.order.routers_order import router_order
from entities.category.routers_category import router_category
from entities.users.routers.client_routers import router_client
from entities.users.routers.employee_routers import router_employee
from entities.service_name.routers_service_name import router_service

routers_all = [
    router_index,
    router_category,
    router_client,
    router_employee,
    router_service,
    router_offer,
    router_order,
]

if i_config.DEBUG:
    routers_all.append(router_init_stub)
