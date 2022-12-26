from fastapi import FastAPI

from admin import CityAdmin     # show in admin page
from core.site_admin import site
from routers.city_routers import router
from routers.index import router_index

app = FastAPI()

# mount AdminSite instance
site.mount_app(app)

app.include_router(router_index)  # , prefix="/api/auth", tags=["auth"]
app.include_router(router)


@app.on_event("startup")
async def startup():
    # Mount the background management system
    print("@" * 80)
