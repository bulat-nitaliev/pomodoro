import json
import pytest
from dataclasses import dataclass
from redis import asyncio as Redis
from app.tasks.schema import TasksSchema


@dataclass
class FakeTaskCache:
    redis: Redis

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_tasks(self) -> list[TasksSchema]:
        async with self.redis as redis:
            tasks = await redis.lrange("tasks", 0, -1)

            if tasks:
                return [TasksSchema.model_validate(json.loads(task)) for task in tasks]
            return []

    async def set_tasks(self, tasks: list[TasksSchema]):
        task_json = [task.model_dump_json() for task in tasks]
        async with self.redis as redis:
            await redis.expire("tasks", 60)
            await redis.lpush("tasks", *task_json)

    async def drop_tasks(self):
        async with self.redis as redis:
            await redis.delete("tasks")


@pytest.fixture
def task_cache(test_cache_get_connect):
    return FakeTaskCache(redis=test_cache_get_connect)
