import orjson
import decimal


def _default(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError


def json_dumps(data) -> str:
    if isinstance(data, list):
        data = orjson.dumps([i.dict() for i in data], default=_default)
    else:
        data = data.json()
    return data


def json_loads(data: str):
    return orjson.loads(data)
