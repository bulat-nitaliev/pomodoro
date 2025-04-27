from sqlalchemy.ext.asyncio import AsyncSession
from core import UserProfile
from sqlalchemy import insert, Result, select, update
from core import db_helper, Tasks
from schema import UserLoginSchema
from dataclasses import dataclass

@dataclass
class UserRepository:
    db_session:AsyncSession

    async def create_user(self,
            username:str,
            password:str
            )->UserProfile:
        query = insert(UserProfile).values(
            username=username,
            password=password
        ).returning(UserProfile.id)
        async with self.db_session as session:
            user_id:int = await session.execute(query)
            await session.commit()
            await session.flush()
            user = await self.get_user_by_id(user_id.scalar())
            return user
        
    async def get_user_by_id(self,user_id:int)->UserProfile:
        query = await select(UserProfile).where(UserProfile.id == user_id)
        async with self.db_session as session:
            return  (await session.execute(query)).scalar_one_or_none()
        
    async def get_user_by_username(self, username:str):
        query = select(UserProfile).where(UserProfile.username == username)
        async with self.db_session as session:
            return  (await session.execute(query)).scalar_one_or_none()
            