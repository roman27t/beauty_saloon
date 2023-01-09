from fastapi import FastAPI
from sqladmin import Admin

from admin import admin_classes
from routers import routers_all
from routers.index import router_index
from models.database import engine

app = FastAPI()

admin = Admin(app, engine)
for admin_class in admin_classes:
    admin.add_view(admin_class)

app.include_router(router_index)
for route in routers_all:
    app.include_router(route)  # , prefix='/api/auth', tags=['auth']


@app.on_event('startup')
async def startup():
    # Mount the background management system
    print('@' * 80)
