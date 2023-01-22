from config import i_config
from routers.index import router_index
from routers.stub_init_routers import router_init_stub

routers_all = [
    router_index,
]
if i_config.DEBUG:
    routers_all.append(router_init_stub)
