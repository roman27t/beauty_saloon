from fastapi import FastAPI
from sqladmin import Admin

from admin import admin_classes
from routers.employee_routers import router
from routers.index import router_index
from routers.stub_init_routers import router_init_stub
from models.database import engine
from config import i_config

app = FastAPI()

admin = Admin(app, engine)
for admin_class in admin_classes:
    admin.add_view(admin_class)

app.include_router(router_index)  # , prefix='/api/auth', tags=['auth']
app.include_router(router)
if i_config.DEBUG:
    app.include_router(router_init_stub)


@app.on_event('startup')
async def startup():
    # Mount the background management system
    print('@' * 80)
