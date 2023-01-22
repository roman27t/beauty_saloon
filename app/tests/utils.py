import typing
import datetime as dt

from main import app
from entities.users.choices_user import Gender


def url_reverse(view_name: str, **path_params: typing.Any) -> str:
    return app.url_path_for(view_name, **path_params)


def user_data() -> dict[str, str]:
    return {
        'phone': '+380983827777',
        'email': 'employee@gmail.com',
        'last_name': 'Dobruden',
        'first_name': 'Hanna',
        'birth_date': dt.datetime.strptime('10.02.1989', '%d.%m.%Y'),
        'gender': Gender.FEMALE,
    }
