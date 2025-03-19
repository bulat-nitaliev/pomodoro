from dataclasses import dataclass
from schema import UserLoginSchema
from repositories import UserRepository
from exception import UserNotFoundException, UserNotCorrectPasswordException

@dataclass
class AuthService:
    user_repository: UserRepository

    def login(self,username:str, password:str)->UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)