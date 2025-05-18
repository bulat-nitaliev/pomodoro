import pytest_asyncio

from app.users import AuthService
from app.config import Settings
from app.users import MailClient
from app.dependecy import get_broker_producer


@pytest_asyncio.fixture
async def auth_service(user_repository, google_client, yandex_client):
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=MailClient(
            settings=Settings(),
            broker_producer=await get_broker_producer(),
        ),
    )
