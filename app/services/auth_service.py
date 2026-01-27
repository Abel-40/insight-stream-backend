from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from pydantic import EmailStr
from uuid import UUID
from core.security import verify_password
async def get_user_by_id(db:AsyncSession,id:UUID)-> User | None:
  stm = select(User).where(User.id == id)
  user = await db.scalar(stm)
  return user

async def get_user_by_email(db:AsyncSession,email:EmailStr)-> User | None:
  stm = select(User).where(User.email == email)
  user = await db.scalar(stm)
  return user

async def local_authenticate(db:AsyncSession, email:EmailStr,password:str):
  user = await get_user_by_email(db=db,email=email)
  if not user:
    return False
  if not verify_password(password,user.hashed_password):
    return False
  return user

