from redis import asyncio as Redis
from typing import List
from app.tasks.schema import TasksSchema

import json


class TaskCache:
    def __init__(self, redis:Redis):
        self.redis = redis

    async def get_tasks(self)->List[TasksSchema]:
        async with self.redis as redis:
            tasks = await redis.lrange('tasks', 0, -1)
            if tasks:
                return  [TasksSchema.model_validate(json.loads(task)) for task in tasks]
            return []
        
    async def set_tasks(self,tasks:List[TasksSchema]):
        task_json = [task.json() for task in tasks]
        async with self.redis as redis:
            await redis.expire('tasks', 60)
            await redis.lpush('tasks', *task_json)

    async def drop_tasks(self):
        async with self.redis as redis:
            await redis.delete('tasks')



        

