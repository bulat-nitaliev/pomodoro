import asyncio
import json
from app.broker import BrokerProducer, BrokerConsumer
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from app.users import (
    UserService,
    AuthService,
    UserRepository,
    GoogleClient,
    YandexClient,
    MailClient,
)
from app.tasks import TaskService, TasksRepository, TaskCache
from fastapi import Depends, Request, security, Security, HTTPException, status
from app.infrastructure import helper, get_connect
from app.config import Settings
from app.exception import TokenException
import httpx
from sqlalchemy.ext.asyncio import AsyncSession


event_loop = asyncio.get_event_loop()


async def get_broker_producer() -> BrokerProducer:
    settings = Settings()
    return BrokerProducer(
        producer=AIOKafkaProducer(
            bootstrap_servers=settings.BROKER_URL, loop=event_loop
        ),
        email_topic=settings.EMAIL_TOPIC,
    )


async def get_broker_consumer() -> BrokerConsumer:
    settings = Settings()
    return BrokerConsumer(
        consumer=AIOKafkaConsumer(
            settings.EMAIL_CALLBACK_TOPIC,
            bootstrap_servers="localhost:9092",
            value_deserializer=lambda message: json.loads(message.decode("utf-8")),
        ),
    )


async def get_mail_client(
    broker_producer: BrokerProducer = Depends(get_broker_producer),
) -> MailClient:
    return MailClient(settings=Settings(), broker_producer=broker_producer)


async def get_db_session():
    async with helper.session_factory() as session:
        yield session


async def get_task_repository(db_session: AsyncSession = Depends(get_db_session)):
    return TasksRepository(db_session=db_session)


def get_task_cache_repository() -> TaskCache:
    redis_connect = get_connect()
    return TaskCache(redis_connect)


def get_task_servise(
    task_repo: TasksRepository = Depends(get_task_repository),
    task_cache: TaskCache = Depends(get_task_cache_repository),
) -> TaskService:
    return TaskService(task_repo=task_repo, task_cache=task_cache)


async def get_user_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


async def get_google_client(
    async_client: httpx.AsyncClient = Depends(get_async_client),
) -> GoogleClient:
    return GoogleClient(settings=Settings(), async_client=async_client)


async def get_yandex_client(
    async_client: httpx.AsyncClient = Depends(get_async_client),
) -> YandexClient:
    return YandexClient(settings=Settings(), async_client=async_client)


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    google_client: GoogleClient = Depends(get_google_client),
    yandex_client: YandexClient = Depends(get_yandex_client),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=MailClient(settings=Settings()),
    )


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reuseable_oauth = security.HTTPBearer()


async def get_request_user_id(
    request: Request,
    token: security.http.HTTPAuthorizationCredentials = Security(reuseable_oauth),
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    return user_id
