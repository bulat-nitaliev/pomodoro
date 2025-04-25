from redis import asyncio as redis
from core import settings

def get_connect()->redis.Redis:
    return redis.Redis(
        host=settings.CACHE_HOST,
        port=settings.CACHE_PORT,
        db=settings.CACHE_DB,
    )

