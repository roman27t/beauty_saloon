from typing import Union, List

from core.utils.redis_interface import i_redis


async def task_clear_cache(keys: Union[str, List[str]]):
    await i_redis.delete(keys)
