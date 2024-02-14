from redis import asyncio as aioredis

from utils.config import Settings

HOST = Settings.get_env("REDIS_HOST")
PORT = Settings.get_env("REDIS_PORT")
DATABASE = Settings.get_env("REDIS_DATABASE")

REDIS_URL = f"redis://{HOST}:{PORT}/{DATABASE}"

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