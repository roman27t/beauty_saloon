from fastapi import FastAPI
from sqladmin import Admin

from admin import admin_classes
from config import i_config
from routers.index import router_index
from models.database import engine
from routers.client_routers import router_client
from routers.offer_routers import offer_service
from routers.service_routers import router_service
from routers.category_routers import router_category
from routers.employee_routers import router
from routers.stub_init_routers import router_init_stub

app = FastAPI()

admin = Admin(app, engine)
for admin_class in admin_classes:
    admin.add_view(admin_class)

app.include_router(router_index)  # , prefix='/api/auth', tags=['auth']
app.include_router(router)
app.include_router(router_service)
app.include_router(offer_service)
app.include_router(router_category)
app.include_router(router_client)
if i_config.DEBUG:
    app.include_router(router_init_stub)


@app.on_event('startup')
async def startup():
    # Mount the background management system
    print('@' * 80)
