from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.tasks.handler import router as task_router
from app.users.user_profile.handler import router as user
from app.users.auth.handlers import router as auth
from app.dependecy import get_broker_consumer
import asyncio



@asynccontextmanager
async def lifespan(app: FastAPI):
    broker_consumer = await get_broker_consumer()
    print(broker_consumer, 1)
    await broker_consumer.consume_callback_message()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user)
app.include_router(auth)
app.include_router(task_router)




# async def send_mail(email:str, message:str):
#     await asyncio.sleep(5)
#     print(f"Email sent to {email} with message: {message}")


# @app.get('/send_mail/')
# async def send_mail_async(background:BackgroundTasks, email:str, message:str):
#     background.add_task(send_mail, email=email, message=message)
#     return {"message": "Email will be sent in the background"}




