import random
import datetime as dt
from decimal import Decimal

from models import CategoryModel, OfferLinkModel, ServiceNameModel, OrderModel
from models.choices import Gender
from schemas.user_schemas import ClientInSchema, EmployeeInSchema
from services.base_service import BaseService
from services.client_service import ClientService
from services.order_service import OrderService, BOOKING_TIME_MINUTES
from services.service_service import (
    CategoryService,
    OfferLinkService,
    ServiceNameService,
)
from services.employee_service import EmployeeService

LAST_NAMES = ('Shevchenko', 'Rebrov', 'Zidane', 'Beckham', 'Husin', 'Husiev', 'Golovko', 'Flo', 'Li', 'Voronin')
FIRST_NAMES = ('Andriy', 'Sergei', 'Zineddin', 'David', 'Andriy', 'Oleh', 'Alex', 'Tore Andre', 'Max', 'Andriy')

SERVICE_1 = ('Body', 'Head', 'Face', 'Leg', 'Hand', 'All')
SERVICE_2 = ('Simple', 'Full')
SERVICE_3 = ('Head haircut', 'Head painting', 'Peeling', 'Beard haircut', 'Beard Coloring', 'Full')
CATEGORIES_SERVICE = {
    'Massage': SERVICE_1,
    'Manicure': SERVICE_2,
    'Pedicure': SERVICE_2,
    'Hairdresser': SERVICE_3,
    'Visagiste': SERVICE_2,
    'Solarium': SERVICE_2,
    'SPA': SERVICE_2,
}
CATEGORIES = tuple(CATEGORIES_SERVICE.keys())


class StubInitService(BaseService):
    def init(self):
        self.__init_user()
        self.__init_service_category()
        self.__init_service_name()
        self.__init_offers()
        self.__init_order()

    def __init_user(self):
        user_service = {EmployeeInSchema: EmployeeService, ClientInSchema: ClientService}
        for index_model, user_model in enumerate(user_service.keys()):
            start = 15 if index_model else 10
            for index, i in enumerate(range(start, start + 5)):
                fio_index = index + 5 if index_model else index
                employee_schema = user_model(
                    phone=f'+3809375470{i}',
                    email=f'example_{i}@gmail.com',
                    last_name=LAST_NAMES[fio_index],
                    first_name=FIRST_NAMES[fio_index],
                    birth_date=dt.datetime.strptime(f'{i}.09.1976', '%d.%m.%Y'),
                    gender=Gender.MALE,
                )
                service_class = user_service[user_model]
                service_class(db_session=self.db_session).add_async(schema=employee_schema)

    def __init_service_category(self):
        for service_name in CATEGORIES:
            category_schema = CategoryModel(name=service_name, detail=f'{service_name} detail info')
            CategoryService(db_session=self.db_session).add_async(schema=category_schema)

    def __init_service_name(self):
        # self.db_session.flush()
        for category, services in CATEGORIES_SERVICE.items():
            for index, service_name in enumerate(services):
                category_schema = ServiceNameModel(
                    category_id=CATEGORIES.index(category) + 1,
                    name=service_name,
                    detail=f'{category} {service_name} detail info',
                    price=Decimal(10000) * Decimal(f'1.{index}'),
                )
                ServiceNameService(db_session=self.db_session).add_async(schema=category_schema)

    def __init_offers(self):
        for index_employee, _ in enumerate(LAST_NAMES[:5]):
            for i in range(1, 10):
                schema = OfferLinkModel(
                    employee_id=index_employee + 1,
                    service_name_id=i,
                    rate=Decimal(1) if random.randint(0, 1) else Decimal(f'1.{random.randint(1,9)}'),
                )
                OfferLinkService(db_session=self.db_session).add_async(schema=schema)

    def __init_order(self):
        for j in range(1, 6):
            for i in range(7, 23):
                if i == 12:
                    continue
                schema = OrderModel(
                    employee_id=j,
                    client_id=i % 5 + 1,
                    start_at=dt.datetime.strptime(f'12.06.2023 {i}:00', '%d.%m.%Y %H:%M'),
                    end_at=dt.datetime.strptime(f'12.06.2023 {i+1}:00', '%d.%m.%Y %H:%M'),
                    expired_at=dt.datetime.now() + dt.timedelta(minutes=BOOKING_TIME_MINUTES),
                )
                OrderService(db_session=self.db_session).add_async(schema=schema)
