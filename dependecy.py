
from service import UserService, AuthService,TaskService
from repositories import UserRepository, TasksRepository, TaskCache
from fastapi import Depends, Request, security,Security, HTTPException, status
from core import  Settings, helper
from exception import TokenException
from exception import TokenException
from client import GoogleClient, YandexClient
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from cache import get_connect


async def get_task_repository():
    # db_session:AsyncSession = Depends(helper.session_factory)
    return TasksRepository(db_session=helper.session_factory())


def get_task_cache_repository()->TaskCache:
    redis_connect = get_connect()
    return TaskCache(redis_connect)

def get_task_servise(
        task_repo:TasksRepository = Depends(get_task_repository),
        task_cache: TaskCache = Depends(get_task_cache_repository)
)->TaskService:
    return TaskService(
        task_repo=task_repo,
        task_cache=task_cache
    )

async def get_user_repository(
        # db_session:AsyncSession = Depends(helper.session_dependency)
        )->UserRepository:
    return UserRepository(db_session=helper.session_factory())

async def get_async_client()->httpx.AsyncClient:
    return httpx.AsyncClient()


async def get_google_client(async_client:httpx.AsyncClient = Depends(get_async_client))->GoogleClient:
    return GoogleClient(
        settings=Settings(),
        async_client=async_client
        )

async def get_yandex_client(async_client:httpx.AsyncClient = Depends(get_async_client))->YandexClient:
    return YandexClient(
        settings=Settings(),
        async_client=async_client
    )


async def get_auth_service(
        user_repository:UserRepository = Depends(get_user_repository),
        google_client: GoogleClient = Depends(get_google_client),
        yandex_client: YandexClient = Depends(get_yandex_client)
        )->AuthService:
    return AuthService(
        user_repository=user_repository, 
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client
        )

async def get_user_service(
        user_repository:UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
        )->UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reuseable_oauth  = security.HTTPBearer()

async def get_request_user_id(request:Request,
    token:security.http.HTTPAuthorizationCredentials = Security(reuseable_oauth),
    auth_service:AuthService = Depends(get_auth_service)
):
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )
    return user_id