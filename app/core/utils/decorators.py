import functools

from core.utils.json_helper import json_dumps, json_loads
from core.utils.redis_interface import cache_redis


def cached(expire: int, key: str = '', extra_keys: list[str] = None):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            extra_slug = ''.join([str(kwargs[i]) for i in extra_keys or []])
            key_name = f'{key or func.__name__}{extra_slug}'
            cache_data = await cache_redis.get(key_name)
            if cache_data:
                return json_loads(cache_data)
            response = await func(*args, **kwargs)
            if response:
                await cache_redis.set(key_name, json_dumps(response), expire)
            return response

        return wrapped

    return wrapper
