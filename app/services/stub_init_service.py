import datetime as dt

from models import ServiceCategoryModel
from models.choices import Gender
from schemas.user_schemas import EmployeeInSchema, ClientInSchema
from services.base_service import BaseService
from services.client_service import ClientService
from services.employee_service import EmployeeService
from services.service_service import ServiceCategoryService

LAST_NAMES = ('Shevchenko', 'Rebrov', 'Zidane', 'Beckham', 'Husin', 'Husiev', 'Golovko', 'Flo', 'Li', 'Voronin')
FIRST_NAMES = ('Andriy', 'Sergei', 'Zineddin', 'David', 'Andriy', 'Oleh', 'Alex', 'Tore Andre', 'Max', 'Andriy')
CATEGORIES = ('Massage', 'Manicure', 'Pedicure', 'Hairdresser', 'Visagiste', 'Solarium', 'SPA')


class StubInitService(BaseService):
    def init(self):
        self.__init_user()
        self.__init_service_category()

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
            category_schema = ServiceCategoryModel(name=service_name, detail=f'{service_name} detail info')
            ServiceCategoryService(db_session=self.db_session).add_async(schema=category_schema)
