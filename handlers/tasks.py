from fastapi import APIRouter, Depends, status
from schema import TasksSchema
from repositories import get_task_repository, get_task_cache_repository, TaskCache, TasksRepository
from typing import List
from service import get_task_servise, TaskService


router = APIRouter(tags=["tasks"], prefix='/tasks')

@router.post("")
def create_task(
    task:TasksSchema, 
    task_repo = Depends(get_task_repository),
    task_cache=Depends(get_task_cache_repository)
    ):
    return task_repo.add_task(task, task_cache)


@router.get("", response_model=List[TasksSchema])
def get_task(
    task_service:TaskService = Depends(get_task_servise),
    ):
    return task_service.get_tasks()
    

@router.get("/{task_id}")
def get_task(task_id:int):
    task_repo = get_task_repository()
    return task_repo.get_task(task_id=task_id)

@router.put("/{task_id}")
def put_task(task_id:int,
             task:TasksSchema,
             task_repo = Depends(get_task_repository),
             task_cache=Depends(get_task_cache_repository)
             ):
    return task_repo.update_task(task_id=task_id, task=task, task_cache=task_cache)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy_task(
    task_id:int,
    task_repo:TasksRepository = Depends(get_task_repository),
    task_cache:TaskCache=Depends(get_task_cache_repository)
    ):
    
    return task_repo.delete_task(task_id=task_id, task_cache=task_cache)
