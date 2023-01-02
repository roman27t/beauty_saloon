import typing
from main import app

def url_reverse(view_name: str, **path_params: typing.Any) -> str:
    return app.url_path_for(view_name, **path_params)
