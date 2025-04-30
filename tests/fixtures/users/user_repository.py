from tests.fixtures.users.user_model import FakeUserProfile
import pytest

from dataclasses import dataclass


@dataclass
class FakeUserRepository:
    async def get_user_by_username(username:str):
        ...

    async def create_user(username:str,
            password:str):
        return FakeUserProfile()

@pytest.fixture
def user_repository():
    return FakeUserRepository