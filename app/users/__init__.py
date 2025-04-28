from app.users.user_profile.service import UserService
from app.users.user_profile.repositories import UserRepository
from app.users.auth.service import AuthService
from app.users.auth.client import GoogleClient, YandexClient
from fastapi import APIRouter


# user_router = APIRouter()
# user_router.include_router(user)
# user_router.include_router(auth)


__all__ = (
    "UserService",
    "UserRepository",
    "AuthService",
    # "user_router",
    "GoogleClient",
    "YandexClient",
)
