from .user_admin import ClientAdmin, EmployeeAdmin
from .service_admin import ServiceCategoryAdmin, ServiceNameAdmin

admin_classes = (
    EmployeeAdmin,
    ClientAdmin,
    ServiceCategoryAdmin,
    ServiceNameAdmin,
)
