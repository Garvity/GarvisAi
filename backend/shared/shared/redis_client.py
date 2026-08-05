import os

from dotenv import load_dotenv
from redis import asyncio as aioredis

load_dotenv()

redis = aioredis.from_url(os.environ["REDIS_URL"], decode_responses=True)


async def check_connection():
    try:
        await redis.ping()
        print("connected to redis")
    except Exception as err:
        print("error connecting to redis", err)
