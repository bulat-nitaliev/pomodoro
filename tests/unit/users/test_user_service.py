import pytest
from tests.fixtures.users.user_model import FakeUserProfile
from app.users.auth.schema import UserLoginSchema



@pytest.mark.asyncio
async def test_create_user__success(user_service):
    fake_user = FakeUserProfile()
    user_schema = await user_service.create_user(
        username=fake_user.username, 
        password=fake_user.password
        )
    
    
    assert isinstance(user_schema, UserLoginSchema)

    