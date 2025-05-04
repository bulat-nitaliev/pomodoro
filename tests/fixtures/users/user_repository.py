from tests.fixtures.users.user_model import FakeUserProfile
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from app.users.user_profile.models import UserProfile

from dataclasses import dataclass


@dataclass
class FakeUserRepository:
    db_session:AsyncSession

    async def get_user_by_username(self,username:str):
        query = select(UserProfile).where(UserProfile.username == username)
        async with self.db_session as session:
            return  (await session.execute(query)).scalar_one_or_none()

    async def create_user(self,username:str,
            password:str
            ):
        query = insert(UserProfile).values(
            username=username,
            password=password
        ).returning(UserProfile.id)
        async with self.db_session as session:
            user_id:int = await session.execute(query)
            
            await session.commit()
            user = await self.get_user_by_id(user_id.scalar())
            return user
        
    async def get_user_by_id(self,user_id:int)->UserProfile:
        query = select(UserProfile).where(UserProfile.id == user_id)
        async with self.db_session as session:
            return  (await session.execute(query)).scalar_one_or_none()
    

@pytest.fixture
def user_repository(get_db_session):
    return FakeUserRepository(db_session=get_db_session)