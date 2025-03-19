from fastapi import Depends, APIRouter
from schema import UserCreateSchema, UserLoginSchema
from  dependecy import get_user_service
from service import UserService
from typing import Annotated

router = APIRouter(tags=['user'], prefix='/user')

@router.post('', response_model=UserLoginSchema)
async def create_user(body:UserCreateSchema, user_service:Annotated[UserService,Depends(get_user_service)]):
    return user_service.create_user(body.username, body.password)