from typing import Union

from core.utils.redis_interface import cache_redis


async def task_clear_cache(keys: Union[str, list[str]]):
    await cache_redis.delete(keys)


async def task_clear_db_cache():
    await cache_redis.flushdb()
