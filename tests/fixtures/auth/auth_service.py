import pytest
from app.users import AuthService
from app.config import Settings


@pytest.fixture
def auth_service(user_repository,google_client,yandex_client):
    return AuthService(
        user_repository=user_repository, 
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client
        )