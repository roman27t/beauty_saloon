import datetime as dt
from decimal import Decimal

from services.base_service import BaseService
from entities.offer.models_offer import OfferModel
from entities.order.models_order import OrderModel, OrderDetailModel
from entities.users.choices_user import Gender
from entities.users.schemas_users import ClientInSchema, EmployeeInSchema
from entities.offer.services_offer import OfferService
from entities.order.services_order import (
    BOOKING_TIME_MINUTES,
    OrderService,
    OrderDetailService,
)
from entities.category.models_category import CategoryModel
from entities.category.services_category import CategoryService
from entities.users.services.client_service import ClientService
from entities.users.services.employee_service import EmployeeService
from entities.service_name.models_service_name import ServiceNameModel
from entities.service_name.services_service_name import ServiceNameService

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
T_BOOK_DATE = '12.06.2023'


class StubInitService(BaseService):
    def init(self):
        self._categories = []
        self._services = []

    def save_data_to_db(self):
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
                service_class(db_session=self.db_session).pre_add(schema=employee_schema)

    def __init_service_category(self):
        for service_name in CATEGORIES:
            category_schema = CategoryModel(name=service_name, detail=f'{service_name} detail info')
            self._categories.append(CategoryService(db_session=self.db_session).pre_add(schema=category_schema))

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
                self._services.append(ServiceNameService(db_session=self.db_session).pre_add(schema=category_schema))

    def __init_offers(self):
        for index_employee, _ in enumerate(LAST_NAMES[:5]):
            for i in range(1, 10):
                schema = OfferModel(
                    employee_id=index_employee + 1,
                    service_name_id=i,
                    rate=Decimal(f'1.{index_employee}'),
                )
                OfferService(db_session=self.db_session).pre_add(schema=schema)

    def __init_order(self):
        order_index = 0
        for user_id in range(1, 6):  # by 5
            for hour in range(7, 23):
                if hour in (12, 13):
                    continue
                order_index += 1
                index_service = order_index % len(self._services) - 1
                service: ServiceNameModel = self._services[index_service]
                schema = OrderModel(
                    service_id=self._services.index(service) + 1,
                    employee_id=user_id,
                    client_id=hour % 5 + 1,
                    start_at=dt.datetime.strptime(f'{T_BOOK_DATE} {hour}:00', '%d.%m.%Y %H:%M'),
                    end_at=dt.datetime.strptime(f'{T_BOOK_DATE} {hour+1}:00', '%d.%m.%Y %H:%M'),
                    expired_at=dt.datetime.now() + dt.timedelta(minutes=BOOKING_TIME_MINUTES),
                    price=service.price,  # todo * rate
                    comment=f'comment {hour}:00 - {hour+1}:00',
                )
                OrderService(db_session=self.db_session).pre_add(schema=schema)
                schema_detail = OrderDetailModel(
                    order_id=order_index,
                    category=self._categories[service.category_id - 1].name,
                    name=service.name,
                    detail=service.name,
                )
                OrderDetailService(db_session=self.db_session).pre_add(schema=schema_detail)
