from fastapi_amis_admin.admin import admin
from core.site_admin import site
from models import CityModel


@site.register_admin
class CityAdmin(admin.ModelAdmin):
    page_schema = 'City'
    model = CityModel
