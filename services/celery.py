from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.conf.beat_schedule = {
    "send_daily_notifications": {
        "task": "tasks.send_message_booking_client",
        "schedule": crontab(houre = 6, minute=0),
    },
    "check_active_bookings": {
        "task": "tasks.check_booking",
        "schedule": crontab(minute='*/30'),
    },
}

