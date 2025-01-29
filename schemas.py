from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    appointment_time: datetime

    def remove_tz(self):
        if self.appointment_time.tzinfo is not None:
            self.appointment_time = self.appointment_time.replace(tzinfo=None)
        return self
    
class BookingCreate(BookingBase):
    user_id: int

class BookingResponse(BookingBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class BookingDelete(BaseModel):
    id: int