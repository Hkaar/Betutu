from redis import asyncio as aioredis

from utils.config import Settings

Settings.load_env()

REDIS_URL = Settings.get_env("REDIS_URL")

class RedisManager:
   redis = None

   @classmethod
   async def connect(cls):
      cls.redis = await aioredis.from_url(REDIS_URL)

   @classmethod
   async def disconnect(cls):
      if cls.redis:
         await cls.redis.close()

   @classmethod
   async def get_redis(cls) -> aioredis.Redis:
      if not cls.redis:
         cls.redis = await aioredis.from_url(REDIS_URL)
      return cls.redis
   
async def get_redis() -> aioredis.Redis:
   return await RedisManager.get_redis()