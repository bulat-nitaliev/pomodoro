from dataclasses import dataclass
from schema import UserLoginSchema
from repositories import UserRepository
from exception import UserNotFoundException, UserNotCorrectPasswordException, TokenException
from core import UserProfile, Settings
from jose import jwt, JWTError
from datetime import datetime, timedelta



@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

    def login(self,username:str, password:str)->UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        access_token = self.create_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
    

    @staticmethod
    def validate(user:UserProfile, password:str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

   
    def create_access_token(self, user_id:int):
        dt_expire = (datetime.utcnow() + timedelta(days=7)).timestamp()
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