from dataclasses import dataclass
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.repositories import UserRepository
from app.users.auth.service import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, username: str, password: str) -> UserLoginSchema:

        user = await self.user_repository.create_user(username, password)

        access_token = self.auth_service.create_access_token(user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
