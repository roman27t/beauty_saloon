from fastapi import FastAPI
from routers import router
from core.site_admin import site
from admin import CityAdmin  # show in admin page

app = FastAPI()

# mount AdminSite instance
site.mount_app(app)

app.include_router(router)  # , prefix="/api/auth", tags=["auth"]


@app.on_event("startup")
async def startup():
    # Mount the background management system
    print('@' * 80)
