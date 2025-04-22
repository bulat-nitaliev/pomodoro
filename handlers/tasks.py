from fastapi import APIRouter, Depends, status, HTTPException
from schema import TasksSchema, TasksCreateSchema
from repositories import get_task_repository, get_task_cache_repository, TaskCache, TasksRepository
from typing import List, Annotated
from service import get_task_servise, TaskService
from dependecy import  get_request_user_id
from exception import TaskNotFoundException


router = APIRouter(tags=["tasks"], prefix='/tasks')

@router.post("", response_model=TasksSchema)
def create_task(
    body:TasksCreateSchema, 
    task_service: Annotated[TaskService, Depends(get_task_servise)],
    user_id:Annotated[int,Depends(get_request_user_id)]
    ):
    return task_service.create_task(body, user_id)


@router.get("", response_model=List[TasksSchema])
def get_task(
    task_service:TaskService = Depends(get_task_servise),
    ):
    return task_service.get_tasks()
    

@router.get("/{task_id}")
def get_task(task_id:int):
    task_repo = get_task_repository()
    return task_repo.get_task(task_id=task_id)

@router.put("/{task_id}", response_model=TasksSchema)
def put_task(task_id:int,
            task:TasksCreateSchema,
            task_service: Annotated[TaskService, Depends(get_task_servise)],
            user_id:Annotated[int,Depends(get_request_user_id)]
             ):
    try:
        return task_service.update_task(
            task_id=task_id, 
            task=task, 
            user_id=user_id
            )
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy_task(
    task_id:int,
    task_service: Annotated[TaskService, Depends(get_task_servise)],
    user_id:Annotated[int,Depends(get_request_user_id)]
    ):
    try:
        task_service.delete_task(task_id=task_id, user_id=user_id)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
