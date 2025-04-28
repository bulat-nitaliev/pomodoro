from fastapi import APIRouter, Depends, status, HTTPException
from app.tasks.schema import TasksSchema, TasksCreateSchema
from typing import List, Annotated
from app.tasks.service import  TaskService
from app.dependecy import  get_request_user_id,get_task_servise
from app.exception import TaskNotFoundException


router = APIRouter(tags=["tasks"], prefix='/tasks')

@router.post("", response_model=TasksSchema)
async def create_task(
    body:TasksCreateSchema, 
    task_service: Annotated[TaskService, Depends(get_task_servise)],
    user_id:Annotated[int,Depends(get_request_user_id)]
    ):
    return await task_service.create_task(body=body, user_id=user_id)


@router.get("", response_model=List[TasksSchema])
async def get_task(
    task_service:TaskService = Depends(get_task_servise),
    ):
    try:
        return await task_service.get_tasks()
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    

@router.get("/{task_id}")
async def get_task(
    task_id:int,
    task_service:TaskService = Depends(get_task_servise)
    ):
    try:
        return await task_service.get_task_by_id(task_id=task_id)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.put("/{task_id}", response_model=TasksSchema)
async def put_task(task_id:int,
            body:TasksCreateSchema,
            task_service: Annotated[TaskService, Depends(get_task_servise)],
            user_id:Annotated[int,Depends(get_request_user_id)]
             ):
    try:
        return await task_service.update_task(
            task_id=task_id, 
            task=body, 
            user_id=user_id
            )
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy_task(
    task_id:int,
    task_service: Annotated[TaskService, Depends(get_task_servise)],
    user_id:Annotated[int,Depends(get_request_user_id)]
    ):
    try:
        await task_service.delete_task(task_id=task_id, user_id=user_id)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
