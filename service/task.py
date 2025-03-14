from fastapi import Depends
from dataclasses import dataclass
from repositories import TaskCache, TasksRepository, get_task_cache_repository,get_task_repository
from schema import TasksSchema

@dataclass
class TaskService:
    task_repo: TasksRepository
    task_cache: TaskCache

    def get_tasks(self):
        if task_cache_repo:= self.task_cache.get_tasks():
        
            return task_cache_repo
        tasks =  self.task_repo.get_tasks()
        tasks_shema = [TasksSchema.model_validate(task) for task in tasks]
        self.task_cache.set_tasks(tasks_shema)
        return tasks_shema




def get_task_servise(
        task_repo:TasksRepository = Depends(get_task_repository),
        task_cache: TaskCache = Depends(get_task_cache_repository)
)->TaskService:
    return TaskService(
        task_repo=task_repo,
        task_cache=task_cache
    )