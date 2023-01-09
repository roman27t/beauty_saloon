from config import i_config
from routers.index import router_index
from routers.offer_routers import offer_service
from routers.client_routers import router_client
from routers.service_routers import router_service
from routers.category_routers import router_category
from routers.employee_routers import router
from routers.stub_init_routers import router_init_stub

routers_all = [
    router_index,
    router,
    router_service,
    offer_service,
    router_category,
    router_client,
]
if i_config.DEBUG:
    routers_all.append(router_init_stub)
