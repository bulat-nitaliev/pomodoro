from fastapi import FastAPI,BackgroundTasks
from app.tasks.handler import router as task_router
from app.users.user_profile.handler import router as user
from app.users.auth.handlers import router as auth
import asyncio


app = FastAPI()
app.include_router(user)
app.include_router(auth)
app.include_router(task_router)


async def send_mail(email:str, message:str):
    await asyncio.sleep(5)
    print(f"Email sent to {email} with message: {message}")


@app.get('/send_mail/')
async def send_mail_async(background:BackgroundTasks, email:str, message:str):
    background.add_task(send_mail, email=email, message=message)
    return {"message": "Email will be sent in the background"}




