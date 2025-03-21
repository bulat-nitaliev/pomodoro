from fastapi import APIRouter
from .tasks import router as task_router
from.user import router as user_router
from .auth import router as auth_router

router = APIRouter()

router.include_router(task_router)
router.include_router(user_router)
router.include_router(auth_router)