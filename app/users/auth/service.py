from dataclasses import dataclass
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.repositories import UserRepository
from app.exception import UserNotFoundException, UserNotCorrectPasswordException, TokenException
from app.users.user_profile.models import UserProfile
from app.config import Settings
from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC
from app.users.auth.client import GoogleClient, YandexClient



@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient

    async def login(self,username:str, password:str)->UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        access_token = self.create_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
    
    async def get_google_redirect_url(self)->str:
        return self.settings.get_url_redirect
    

    async def get_yandex_redirect_url(self)->str:
        return self.settings.get_yandex_url_redirect

    async def auth_google(self,code:str)->UserLoginSchema:
        user_info = await  self.google_client.get_user_info(code=code)
        print(user_info)
        user = await self.user_repository.get_user_by_username(username=user_info['email'])
        print(user)
        if user:
            access_token = self.create_access_token(user_id=user.id)
            return UserLoginSchema(
                user_id=user.id, 
                access_token=access_token
                )
        user_created = await self.user_repository.create_user(
            username=user_info['email'],
            password=user_info['name']
        )
        access_token = self.create_access_token(user_id=user_created.id)
        return UserLoginSchema(
            user_id=user_created.id, 
            access_token=access_token
            )


    async def auth_yandex(self, code:str)->UserLoginSchema:
        user_info = await self.yandex_client.get_user_info(code=code)
        print(user_info)
        user = await self.user_repository.get_user_by_username(username=user_info['default_email'])
        print(user)
        if user:
            access_token = self.create_access_token(user_id=user.id)
            return UserLoginSchema(
                user_id=user.id, 
                access_token=access_token
                )
        user_created = await self.user_repository.create_user(
            username=user_info['default_email'],
            password=user_info['login']
        )
        access_token = self.create_access_token(user_id=user_created.id)
        return UserLoginSchema(
            user_id=user_created.id, 
            access_token=access_token
            )


    

    @staticmethod
    def validate(user:UserProfile, password:str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

   
    def create_access_token(self, user_id:int):
        dt_expire = (datetime.now(tz=UTC) + timedelta(days=7)).timestamp()
        token = jwt.encode(
            {'user_id': user_id, 'exp':dt_expire}, 
            self.settings.JWT_SECRET, 
            algorithm=self.settings.JWT_ALGORITM
            )
        return token
    
    def get_user_id_from_access_token(self, access_token):
        try:
            payload = jwt.decode(
                token=access_token, 
                key=self.settings.JWT_SECRET, 
                algorithms=[self.settings.JWT_ALGORITM])
        except JWTError:
            raise TokenException
        return payload['user_id']