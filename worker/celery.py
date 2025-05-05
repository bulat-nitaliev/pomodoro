
from app.config import settings
from celery import Celery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl


app = Celery(__name__)
# app.conf.broker_url = settings.CELERY_BROKER_URL
# app.conf.result_backend = settings.CELERY_RESULT_BACKEND
app.conf.broker_url = settings.BROKER_URL
app.conf.result_backend = 'rpc://'


@app.task(name='send_message')
def send_message(subject:str, text:str, to:str):
    msg = build_message(subject=subject,text=text, to=to)
    send_msg(msg=msg, to=to)



    
def build_message(subject:str,text:str,to)->MIMEMultipart:
    msg = MIMEMultipart()

    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(_text=text))

    return msg


def send_msg(msg:str):
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT, context=context)
    server.login(user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)
    server.send_message(msg=msg)
    server.quit()
