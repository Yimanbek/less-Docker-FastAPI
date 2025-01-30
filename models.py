from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique = True, index=True, nullable = False)
    password = Column(String, index=False, nullable=False)
    
    bookings = relationship('Booking', back_populates='user')

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key = True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    is_active = Column(Boolean)
    appointment_time = Column(DateTime(timezone=True), nullable=False)

    user = relationship('User', back_populates='bookings')