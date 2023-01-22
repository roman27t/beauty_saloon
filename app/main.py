from fastapi import FastAPI
from sqladmin import Admin

from config import i_config
from admins import admin_classes
from routers import routers_all
from models.database import engine

app = FastAPI(debug=i_config.DEBUG)

admin = Admin(app, engine)
for admin_class in admin_classes:
    admin.add_view(admin_class)

for route in routers_all:
    app.include_router(route)  # , prefix='/api/auth', tags=['auth']


if i_config.DEBUG and i_config.DEBUG_TOOLBAR:
    from debug_toolbar.middleware import DebugToolbarMiddleware

    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
    )


@app.on_event('startup')
async def startup():
    # Mount the background management system
    print('@' * 80)
