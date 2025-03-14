from redis import Redis
from typing import List
from schema import TasksSchema
from cache import get_connect
import json


class TaskCache:
    def __init__(self, redis:Redis):
        self.redis = redis

    def get_tasks(self)->List[TasksSchema]:
        with self.redis as redis:
            tasks = redis.lrange('tasks', 0, -1)
            return  [TasksSchema.model_validate(json.loads(task)) for task in tasks]
        
    def set_tasks(self,tasks:List[TasksSchema]):
        task_json = [task.json() for task in tasks]
        with self.redis as redis:
            redis.expire('tasks', 60)
            redis.lpush('tasks', *task_json)

    def drop_tasks(self):
        with self.redis as redis:
            redis.delete('tasks')


def get_task_cache_repository()->TaskCache:
    redis_connect = get_connect()
    return TaskCache(redis_connect)
        

