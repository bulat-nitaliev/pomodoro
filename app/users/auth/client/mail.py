from dataclasses import dataclass
from app.config import Settings
from worker.celery import send_message


@dataclass
class MailClient:
    settings: Settings

    def send_welcome_message(
            self, 
            subject:str, 
            text:str, 
            to:str
            ):
        
        task_id = send_message.delay(
            subject=subject, 
            text=text, 
            to=to
            )
        print(task_id)
        return task_id
