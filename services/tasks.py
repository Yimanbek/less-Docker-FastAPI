from celery import Celery, shared_task
from database import async_session
from models import Booking, User
from sqlalchemy.future import select
from datetime import datetime, timedelta
from .celery_tasks import send_message_to_client_task
import asyncio

app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)


@shared_task
def check_booking():
    async def _run_check():
        async with async_session() as session:
            result = await session.execute(select(Booking).where(Booking.is_active == True))
            bookings = result.scalars().all()

            for booking in bookings:
                if booking.appointment_time < datetime.utcnow():
                    booking.is_active = False
            await session.commit()

    asyncio.run(_run_check())


@shared_task
def send_message_booking_client():
    async def _run_send():
        async with async_session() as session:
            result = await session.execute(select(Booking).where(Booking.is_active == True))
            bookings = result.scalars().all()

            for booking in bookings:
                time_diff = booking.appointment_time - datetime.utcnow()
                if time_diff.total_seconds() < 86400:
                    user = await session.get(User, booking.user_id)
                    send_message_to_client_task.delay(
                        email=user.email,
                        time=booking.appointment_time,
                        warning=True
                    )
    asyncio.run(_run_send())