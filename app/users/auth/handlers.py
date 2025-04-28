from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.schema import UserCreateSchema
from app.users.auth.service import AuthService
from app.dependecy import get_auth_service
from app.exception import UserNotCorrectPasswordException, UserNotFoundException
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["auth"], prefix='/auth')

@router.post('/login', response_model=UserLoginSchema)
async def login(
    body:UserCreateSchema,
    user_service: Annotated[AuthService,Depends(get_auth_service)]
    )->UserLoginSchema:
    try:
        return await user_service.login(body.username, body.password)
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
    


@router.get(
        "/login/google",
        response_class=RedirectResponse
        )
async def google_login(auth_service: Annotated[AuthService,Depends(get_auth_service)]) :
    redirect_url:str =  await auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(url=redirect_url)


@router.get('/google')
async def auth_google(
    auth_service: Annotated[AuthService,Depends(get_auth_service)],
    code:str
):
    return await auth_service.auth_google(code=code)


@router.get('/login/yandex', response_class=RedirectResponse)
async def get_yandex_login(auth_service: Annotated[AuthService,Depends(get_auth_service)]):
    redirect_url:str = await auth_service.get_yandex_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get('/yandex', response_model=UserLoginSchema)
async def auth_yandex(
    auth_service: Annotated[AuthService,Depends(get_auth_service)],
    code:str
):
    return await auth_service.auth_yandex(code=code)