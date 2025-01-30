from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Booking
from schemas import BookingCreate, BookingDelete, BookingResponse
from services.celery_tasks import send_message_to_client_task
from datetime import timedelta
from database import async_session
from models import User

router = APIRouter()

@router.post("/", response_model=BookingResponse)
async def create_booking(data:BookingCreate, db: AsyncSession = Depends(get_db)):
    data = data.remove_tz()
    new_time = data.appointment_time + timedelta(days=1)
    new_booking = Booking(
        user_id = data.user_id,
        appointment_time = new_time,
        is_active=True
    )

    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)
    async with async_session() as session:
        user = await session.get(User, new_booking.user_id)
    send_message_to_client_task.delay(email=user.email, time=new_time, warning=False)
    
    return new_booking

@router.delete('/delete')
async def delete_booking(data:BookingDelete, db: AsyncSession = Depends(get_db)):
    
    stmt = select(Booking).where(Booking.id == data.id)
    result = await db.execute(stmt)
    booking = result.scalar()

    if not booking:
        raise HTTPException(status_code=404, detail = "Запись не найдена")
    
    await db.delete(booking)
    await db.commit()
    return {'message': 'Запись удалена'}