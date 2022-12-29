import datetime as dt
from services.client_service import ClientService
from models import ClientModel, EmployeeModel
from services.base_service import BaseService
from services.city_service import EmployeeService

LAST_NAMES = ('Shevchenko', 'Rebrov', 'Zidane', 'Beckham', 'Husin', 'Husiev', 'Golovko', 'Flo', 'Li', 'Voronin')
FIRST_NAMES = ('Andriy', 'Sergei', 'Zineddin', 'David', 'Andriy', 'Oleh', 'Alex', 'Tore Andre', 'Max', 'Andriy')


class StubInitService(BaseService):
    def init(self):
        user_service = {EmployeeModel: EmployeeService, ClientModel: ClientService}
        for index_model, user_model in enumerate(user_service.keys()):
            start = 15 if index_model else 10
            for index, i in enumerate(range(start, start + 5)):
                fio_index = index + 5 if index_model else index
                employee_schema = user_model(
                    phone=f'+3809375470{i}',
                    email=f'example_{i}@gmail.com',
                    last_name=LAST_NAMES[fio_index],
                    first_name=FIRST_NAMES[fio_index],
                    birthday=dt.datetime.strptime(f'{i}.09.1976', '%d.%m.%Y'),
                )
                service_class = user_service[user_model]
                service_class(db_session=self.db_session).add(employee=employee_schema)