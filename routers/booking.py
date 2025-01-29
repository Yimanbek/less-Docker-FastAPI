from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Booking
from schemas import BookingCreate, BookingDelete, BookingResponse


router = APIRouter()

@router.post("/", response_model=BookingResponse)
async def create_booking(data:BookingCreate, db: AsyncSession = Depends(get_db)):
    data = data.remove_tz()
    new_booking = Booking(
        user_id = data.user_id,
        appointment_time = data.appointment_time
    )

    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)

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