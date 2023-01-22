import orjson
import functools

from core.utils.redis_interface import i_redis


def cached(key: str = '', expire: int = 3600):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            key_name = key or func.__name__
            cache_data = await i_redis.get(key_name)
            if cache_data:
                return orjson.loads(cache_data)
            response = await func(*args, **kwargs)
            if response:
                data = orjson.dumps([i.dict() for i in response])
                await i_redis.set(key_name, data, expire)
            return response

        return wrapped

    return wrapper
