from app.core.db import AsyncLocalSession
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,Request,HTTPException
from typing import Annotated
from jwt.exceptions import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.core.config import settings
from app.services.auth_service import get_user_by_id
import jwt


auth_scheme = OAuth2PasswordBearer(
    tokenUrl="/insight/auth/login/local"
)


async def get_current_user(request:Request,token:Annotated[str,Depends(auth_scheme)],db:AsyncSession = Depends(get_db)):
  credentials_exception = HTTPException(status_code=401,detail="Invalid Credentials!!!", headers = {"WWW-Authenticate":"Bearer"})
  try:
    payload = jwt.decode(token,settings.ACCESS_KEY,algorithms=[settings.ALGO])
    user_id = payload.get("sub")
    if not user_id or payload.get("type") != "access":
      raise credentials_exception
  except PyJWTError as e:
    print("JWT ERROR TYPE:", type(e).__name__)
    print("JWT ERROR MSG:", str(e))
    raise credentials_exception
  user = await get_user_by_id(db=db,id=user_id)
  if not user:
    raise credentials_exception
  request.state.user_id = user.id
  return user