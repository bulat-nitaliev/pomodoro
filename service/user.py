from dataclasses import dataclass
from schema import UserLoginSchema
from repositories import UserRepository
from service.auth import AuthService

@dataclass
class UserService:
    user_repository:UserRepository
    auth_service: AuthService


    def create_user(self,username:str, password:str)->UserLoginSchema:
        
        user = self.user_repository.create_user(username, password)
        access_token = self.auth_service.create_access_token(user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
    
    
