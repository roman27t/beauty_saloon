from typing import Union
from dataclasses import dataclass

import aioredis

from config import i_config


@dataclass(frozen=True)
class RedisDb:
    CACHE = 1


class RedisInterface:
    def __init__(self, db: int = RedisDb.CACHE):
        self._db = db
        self._con = self.init()

    def init(self):
        return aioredis.Redis(
            host=i_config.REDIS_HOST,
            port=i_config.REDIS_PORT,
            password=i_config.REDIS_PASSWORD,
            socket_timeout=i_config.REDIS_TIMEOUT,
            db=self._db,
        )

    async def set(self, key: str, value: str, expire: int):
        return await self._con.set(key, value, expire)

    async def get(self, key: str):
        return await self._con.get(key)

    async def delete(self, *keys: Union[str, list[str]]):
        return await self._con.delete(*keys)

    async def close(self):
        await self._con.close()

    async def flushall(self):
        await self._con.flushall()

    async def flushdb(self):
        await self._con.flushdb()

    async def keys(self, pattern):
        return await self._con.keys(pattern)


cache_redis = RedisInterface()
