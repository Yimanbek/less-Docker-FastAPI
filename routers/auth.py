from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 
from database import get_db
from models import User
from schemas import UserCreate, UserResponse
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hash_password(password: str):
    return pwd_context.hash(password)

@router.post('/register', response_model=UserResponse)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == data.email)
    result = await db.execute(stmt)
    existing_email = result.scalars().first()

    if existing_email:
        raise HTTPException(status_code=400, detail = 'Пользовател уже существует')
    
    new_user = User(email = data.email, password = hash_password(data.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user