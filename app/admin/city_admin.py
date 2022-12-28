from fastapi_amis_admin.admin import admin

from core.site_admin import site
from models import EmployeeModel, ClientModel


@site.register_admin
class EmployeeAdmin(admin.ModelAdmin):
    page_schema = 'Employee'
    model = EmployeeModel

    list_display = [EmployeeModel.id]


# @site.register_admin
# class ClientAdmin(admin.ModelAdmin):
#     page_schema = 'Client'
#     model = ClientModel
#
#     list_display = [ClientModel.id]
