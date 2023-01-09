from .user_model import ClientModel, EmployeeModel
from .offer_model import OfferLinkModel
from .service_model import CategoryModel, ServiceNameModel

# User [Client, Master] (email)
# -------------
# + email
# + phone
# + first_name
# + last_name
# + birthday
# + is_active: Union[bool, None] = True

# Service (type_service, name)
# -------------
# name
# amount
# description
# type_service ?

# Master-Service
# Master
# Service


# Order
# ------
# Client
# Master
# Log_Order
# is_active
# date_start
# date_end

# Log_Order
# -------------
# amount
# description   [Service]
# comment
# name
# type_service

# Notification
# ---------------
# Order
# type_notification
