from sqlalchemy.orm import Session
from service import UserService, AuthService
from repositories import UserRepository
from fastapi import Depends, Request, security,Security, HTTPException, status
from core import get_db_session, Settings
from exception import TokenException
from exception import TokenException
from client import GoogleClient


def get_user_repository(
        db_session:Session = Depends(get_db_session)
        )->UserRepository:
    return UserRepository(db_session=db_session)


def get_google_client()->GoogleClient:
    return GoogleClient(Settings())


def get_auth_service(
        user_repository:UserRepository = Depends(get_user_repository),
        google_client: GoogleClient = Depends(get_google_client)
        )->AuthService:
    return AuthService(
        user_repository=user_repository, 
        settings=Settings(),
        google_client=google_client
        )

def get_user_service(
        user_repository:UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
        )->UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reuseable_oauth  = security.HTTPBearer()

def get_request_user_id(request:Request,
    token:security.http.HTTPAuthorizationCredentials = Security(reuseable_oauth),
    auth_service:AuthService = Depends(get_auth_service)
):
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )
    return user_id