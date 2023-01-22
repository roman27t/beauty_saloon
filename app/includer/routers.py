from entities.category.routers_category import router_category
from entities.service_name.service_routers import router_service
from entities.users.routers.client_routers import router_client
from entities.users.routers.employee_routers import router_employee

routers_all2 = [
    router_category,
    router_client,
    router_employee,
    router_service,
]
