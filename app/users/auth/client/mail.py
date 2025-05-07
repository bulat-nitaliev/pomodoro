from dataclasses import dataclass
from app.config import Settings
# from worker.celery import send_message
import aio_pika
import json
import uuid


@dataclass
class MailClient:
    settings: Settings

    async def send_welcome_message(
            self, 
            subject:str, 
            text:str, 
            to:str
            ):
        
        connection = await aio_pika.connect_robust(self.settings.BROKER_URL)
        print(connection, self.settings.BROKER_URL)
        async with connection:
            channel = await connection.channel()
            data = {
                "message": text,
                "user_email": to,
                "subject": subject
            }
            message  = aio_pika.Message(
                body=json.dumps(data).encode(),
                correlation_id=str(uuid.uuid4())
            )
            name ='email_queue'
            await channel.declare_queue(name,durable=True)

            await channel.default_exchange.publish(
                message=message,
                routing_key=name
            )
            return
            
                
            

