from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from schema import UserLoginSchema,UserCreateSchema
from service import AuthService
from dependecy import get_auth_service
from exception import UserNotCorrectPasswordException, UserNotFoundException


router = APIRouter(tags=["auth"], prefix='/auth')

@router.post('/login', response_model=UserLoginSchema)
async def login(
    body:UserCreateSchema,
    user_service: Annotated[AuthService,Depends(get_auth_service)]
    )->UserLoginSchema:
    try:
        return user_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except UserNotCorrectPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )