from typing import List, Union

from core.utils.redis_interface import i_redis


async def task_clear_cache(keys: Union[str, List[str]]):
    await i_redis.delete(keys)


async def task_clear_db_cache():
    await i_redis.flushdb()