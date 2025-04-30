import pytest
from app.users import UserService
from app.config import Settings


@pytest.fixture
def user_service(user_repository,auth_service):
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service
        )