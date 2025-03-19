from dataclasses import dataclass
from schema import UserLoginSchema
from repositories import UserRepository
from random import choice
from string import ascii_uppercase, digits

@dataclass
class UserService:
    user_repository:UserRepository


    def create_user(self,username:str, password:str)->UserLoginSchema:
        access_token = self._create_access_token()
        user = self.user_repository.create_user(username, password, access_token)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
    
    @staticmethod
    def _create_access_token():
        return ''.join(choice(ascii_uppercase+digits) for _ in range(10))
