from typing import List

import orjson
import decimal
import functools

from core.utils.redis_interface import i_redis


def default(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError


def cached(key: str = '', expire: int = 3600, extra_keys: List[str] = None):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            extra_slug = ''.join([str(kwargs[i]) for i in extra_keys or []])
            key_name = f'{key or func.__name__}{extra_slug}'
            cache_data = await i_redis.get(key_name)
            if cache_data:
                return orjson.loads(cache_data)
            response = await func(*args, **kwargs)
            if response:
                data = orjson.dumps([i.dict() for i in response], default=default)
                await i_redis.set(key_name, data, expire)
            return response

        return wrapped

    return wrapper
