from dataclasses import dataclass
from app.config import Settings
# from worker.celery import send_message
import aio_pika
import json
import uuid
from app.broker import BrokerProducer


@dataclass
class MailClient:
    settings: Settings
    broker_producer: BrokerProducer

    async def send_welcome_message(
            self, 
            subject:str, 
            text:str, 
            to:str
            ):
        data = {
                "message": text,
                "user_email": to,
                "subject": subject,
                "correllation_id": str(uuid.uuid4())
            }
        
        await self.broker_producer.send_welkome_email(email_data=data)
        
        
            
                
            

