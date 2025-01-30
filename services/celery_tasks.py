from celery import Celery
from .send_email import send_message_to_client

celery_app = Celery("tasks", 
                    broker="redis://redis:6379/0", 
                    backend="redis://redis:6379/0")

@celery_app.task
def send_message_to_client_task(email: str, warning=False, time=None):
    send_message_to_client(email, warning, time)