from fastapi import FastAPI
from app.tasks.handler import router as task_router
from app.users.user_profile.handler import router as user
from app.users.auth.handlers import router as auth


app = FastAPI()
app.include_router(user)
app.include_router(auth)
app.include_router(task_router)



