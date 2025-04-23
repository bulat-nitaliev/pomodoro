from fastapi import Depends
from dataclasses import dataclass
from repositories import TaskCache, TasksRepository, get_task_cache_repository,get_task_repository
from schema import TasksSchema,TasksCreateSchema
from exception import TaskNotFoundException

@dataclass
class TaskService:
    task_repo: TasksRepository
    task_cache: TaskCache

    def get_tasks(self):
        if task_cache_repo:= self.task_cache.get_tasks():
            print(task_cache_repo)
        
            return task_cache_repo
        tasks =  self.task_repo.get_tasks()
        tasks_shema = [TasksSchema.model_validate(task) for task in tasks]
        self.task_cache.set_tasks(tasks_shema)
        return tasks_shema
    

    def create_task(self, body:TasksCreateSchema,user_id:int)->TasksSchema:
        task_id = self.task_repo.add_task(
            task=body, 
            task_cache=self.task_cache, 
            user_id=user_id
            )
        task = self.task_repo.get_task(task_id=task_id)
        return TasksSchema.model_validate(task)
    
    def update_task(
            self, 
            task_id:int, 
            task:TasksCreateSchema, 
            user_id:int
            ):
        task_current = self.task_repo.get_user_task(task_id=task_id, user_id=user_id)
        if not task_current:
            raise TaskNotFoundException
        task_update = self.task_repo.update_task(
            task_id=task_id,
            task=task, 
            task_cache=self.task_cache,
            user_id=user_id
            )
        return TasksSchema.model_validate(task_update)
    
    
    def delete_task(self, task_id:int, user_id:int):
        task = self.task_repo.get_user_task(task_id=task_id, user_id=user_id)
        if not task:
            raise TaskNotFoundException
        self.task_repo.delete_task(
            task_id=task_id,
            task_cache=self.task_cache
        )
    





def get_task_servise(
        task_repo:TasksRepository = Depends(get_task_repository),
        task_cache: TaskCache = Depends(get_task_cache_repository)
)->TaskService:
    return TaskService(
        task_repo=task_repo,
        task_cache=task_cache
    )