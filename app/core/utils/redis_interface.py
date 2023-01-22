from typing import Optional

import aioredis
from config import i_config


class RedisInterface:
    def __init__(self, db: int = 1):
        self.db = db
        self._con = self.init()

    def init(self):
        return aioredis.Redis(
        host=i_config.REDIS_HOST,
        port=i_config.REDIS_PORT,
        password=i_config.REDIS_PASSWORD,
        socket_timeout=i_config.REDIS_TIMEOUT,
        db=self.db,
    )

    async def set(self, key, value, expire: int):
        return await self._con.set(key, value, expire)

    async def get(self, key):
        return await self._con.get(key)

    async def close(self):
        await self._con.close()

    async def flushall(self):
        await self._con.flushall()

    async def keys(self, pattern):
        return await self._con.keys(pattern)


i_redis = RedisInterface()
