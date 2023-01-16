from config import i_config
from routers.index import router_index
from routers.offer_routers import router_offer
from routers.order_routers import router_order
from routers.offer_full_routers import router_offer_full
from routers.client_routers import router_client
from routers.service_routers import router_service
from routers.category_routers import router_category
from routers.employee_routers import router_employee
from routers.stub_init_routers import router_init_stub

routers_all = [
    router_index,
    router_employee,
    router_client,
    router_category,
    router_service,
    router_offer,
    router_offer_full,
    router_order,
]
if i_config.DEBUG:
    routers_all.append(router_init_stub)
