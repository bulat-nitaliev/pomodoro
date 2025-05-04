import pytest
from app.users.user_profile.models import UserProfile
from sqlalchemy import select, insert
from tests.fixtures.users.user_model import EXISTS_GOOGLE_USER, EXISTS_GOOGLE_PASSWORD


@pytest.mark.asyncio
async def test_google_auth_not_exists_user(auth_service, get_db_session):

    async with get_db_session as session:
        users_db = (await session.execute(select(UserProfile))).scalars().all()
        

    user = await auth_service.auth_google(code='fake code')


    assert len(users_db) == 0
    assert user is not None

    async with get_db_session as session:
        login_user = (await session.execute(select(UserProfile).where(UserProfile.id == user.user_id))).scalars().first()
        
    assert login_user.id == user.user_id


@pytest.mark.asyncio
async def test_google_auth__login_exist_user(auth_service, get_db_session):
    query = insert(UserProfile).values(
        username=EXISTS_GOOGLE_USER,
        password=EXISTS_GOOGLE_PASSWORD
    )
    code = "fake_code"
    

    async with get_db_session as session:
        await session.execute(query)
        await session.commit()
        user_data = await auth_service.auth_google(code)
        login_user = (await session.execute(select(UserProfile).where(UserProfile.id == user_data.user_id))).scalar_one_or_none()

    assert login_user.username == EXISTS_GOOGLE_USER
    assert user_data.user_id == login_user.id


@pytest.mark.asyncio
async def test_base_login__success(auth_service, get_db_session):
    username = "test_username"
    password = "test_password"

    query = insert(UserProfile).values(
        username=username,
        password=password
    )

    
    async with get_db_session as session:
        await session.execute(query)
        await session.commit()
        await session.flush()
        login_user = (await session.execute(select(UserProfile).where(UserProfile.username == username))).scalar_one_or_none()

    user_data = await auth_service.login(username=username, password=password)

    assert login_user is not None
    assert user_data.user_id == login_user.id