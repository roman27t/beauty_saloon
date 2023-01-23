from typing import List, Union

from core.utils.redis_interface import cache_redis


async def task_clear_cache(keys: Union[str, List[str]]):
    await cache_redis.delete(keys)


async def task_clear_db_cache():
    await cache_redis.flushdb()
