from sqlalchemy.orm import Session
from core import UserProfile
from sqlalchemy import insert, Result, select, update
from core import db_helper, Tasks
from schema import UserLoginSchema
from dataclasses import dataclass


@dataclass
class UserRepository:
    db_session:Session

    def create_user(self,
            username:str,
            password:str,
            access_token:str
            )->UserProfile:
        query = insert(UserProfile).values(
            username=username,
            password=password,
            access_token=access_token
        ).returning(UserProfile.id)
        with self.db_session as session:
            user_id:int = session.execute(query).scalar()
            session.commit()
            session.flush()
            user = self.get_user_by_id(user_id)
            return user
        
    def get_user_by_id(self,user_id:int)->UserProfile:
        query = select(UserProfile).where(UserProfile.id == user_id)
        with self.db_session as session:
            return  session.execute(query).scalar_one_or_none()
        
    def get_user_by_username(self, username:str):
        query = select(UserProfile).where(UserProfile.username == username)
        with self.db_session as session:
            return  session.execute(query).scalar_one_or_none()
            