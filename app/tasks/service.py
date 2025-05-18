from dataclasses import dataclass
from app.tasks.repositories import TaskCache, TasksRepository
from app.tasks.schema import TasksSchema, TasksCreateSchema
from app.exception import TaskNotFoundException


@dataclass
class TaskService:
    task_repo: TasksRepository
    task_cache: TaskCache

    async def get_tasks(self):

        if task_cache_repo := await self.task_cache.get_tasks():
            print(task_cache_repo, "cache_______")
            return task_cache_repo

        tasks = await self.task_repo.get_tasks()
        tasks_shema = [TasksSchema.model_validate(task) for task in tasks]
        if tasks_shema:
            await self.task_cache.set_tasks(tasks_shema)
        return tasks_shema

    async def get_task_by_id(self, task_id: int) -> TasksSchema:
        task = await self.task_repo.get_task(task_id=task_id)
        if task:
            return TasksSchema.model_validate(task)
        raise TaskNotFoundException

    async def create_task(self, body: TasksCreateSchema, user_id: int) -> TasksSchema:
        task_id = await self.task_repo.add_task(
            task=body, task_cache=self.task_cache, user_id=user_id
        )

        task = await self.task_repo.get_task(task_id=task_id)
        return TasksSchema.model_validate(task)

    async def update_task(self, task_id: int, task: TasksCreateSchema, user_id: int):
        task_current = await self.task_repo.get_user_task(
            task_id=task_id, user_id=user_id
        )
        if not task_current:
            raise TaskNotFoundException
        task_update = await self.task_repo.update_task(
            task_id=task_id, task=task, task_cache=self.task_cache, user_id=user_id
        )

        return TasksSchema.model_validate(task_update)

    async def delete_task(self, task_id: int, user_id: int):
        task = await self.task_repo.get_user_task(task_id=task_id, user_id=user_id)
        if not task:
            raise TaskNotFoundException
        await self.task_repo.delete_task(task_id=task_id, task_cache=self.task_cache)
