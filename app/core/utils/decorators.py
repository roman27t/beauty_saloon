from typing import List

import functools

from core.json_helper import json_dumps, json_loads
from core.utils.redis_interface import i_redis


def cached(key: str = '', expire: int = 3600, extra_keys: List[str] = None):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            extra_slug = ''.join([str(kwargs[i]) for i in extra_keys or []])
            key_name = f'{key or func.__name__}{extra_slug}'
            cache_data = await i_redis.get(key_name)
            if cache_data:
                return json_loads(cache_data)
            response = await func(*args, **kwargs)
            if response:
                await i_redis.set(key_name, json_dumps(response), expire)
            return response

        return wrapped

    return wrapper
