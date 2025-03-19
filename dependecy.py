from sqlalchemy.orm import Session
from service import UserService, AuthService
from repositories import UserRepository
from fastapi import Depends
from core import get_db_session


def get_user_repository(
        db_session:Session = Depends(get_db_session)
        )->UserRepository:
    return UserRepository(db_session=db_session)

def get_user_service(user_repository:UserRepository = Depends(get_user_repository))->UserService:
    return UserService(user_repository=user_repository)


def get_auth_service(user_repository:UserRepository = Depends(get_user_repository))->AuthService:
    return AuthService(user_repository=user_repository)