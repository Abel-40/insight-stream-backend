from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User,AuthAccount
from app.schemas.user import UserInForDb,ThirdPartyLogin,LocalLogin
from pydantic import EmailStr
from uuid import UUID
from app.core.security import verify_password
from app.exceptions.auth_exceptions import EmailAlreadyExistsError,InvalidCredentialsError
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

async def register_local_user(user_data:UserInForDb,db:AsyncSession):
  existing_email = (await db.scalars(
    select(User)
    .where(User.email == user_data.email)
    )).one_or_none()
  if existing_email:
    raise EmailAlreadyExistsError
  user = User(**user_data.model_dump(exclude_none=True))
  db.add(user)
  await db.flush()
  
  await db.refresh(user)
  authAccount = AuthAccount(provider="local",provider_account_id=user.email,user_id=user.id)
  db.add(authAccount)
  await db.commit()
  
  return user

async def login_with_third_party(user_data:ThirdPartyLogin,db:AsyncSession):
  existing_auth_account = await db.scalars(
    select(AuthAccount).where(provider=user_data.provider,provider_account_id=user_data.provider_account_id)
  ).one_or_none()
  if existing_auth_account:
    return existing_auth_account.user
  user = User(email=user_data.email)
  db.add(User)
  await db.flush()
  
  await db.refresh(user)
  auth_account = AuthAccount(provider=user_data.provider,provider_account_id=user_data.provider_account_id,user_id=user.id)
  db.add(auth_account)
  await db.commit()
  
  return user

async def local_login(user_data:LocalLogin,db:AsyncSession):
  user = await local_authenticate(email=user_data.email,password=user_data.password,db=db)
  if not user:
    raise InvalidCredentialsError
  return user
  