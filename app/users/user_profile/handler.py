from fastapi import Depends, APIRouter
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.schema import UserCreateSchema
from app.dependecy import get_user_service
from app.users.user_profile.service import UserService
from typing import Annotated


router = APIRouter(tags=["user"], prefix="/user")


@router.post("", response_model=UserLoginSchema)
async def create_user(
    body: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create_user(body.username, body.password)
