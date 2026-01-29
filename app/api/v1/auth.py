from fastapi import APIRouter,Depends,HTTPException,status,Request
from app.services.auth_service import register_local_user,login_with_third_party,authenticate_local_user,get_user_by_id
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import token_generator
from app.core.config import settings
from app.schemas.user import UserInForLocal, UserOut,UserInForDb,ThirdPartyLogin,LocalLogin
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions.auth_exceptions import EmailAlreadyExistsError,InvalidCredentialsError
from app.schemas.token import TokenResponse
from app.schemas.response import APIResponse
from app.core.security import hash_password
from app.dependencies.database import get_db
from app.utils.response import success_response
from datetime import timedelta
from jwt.exceptions import InvalidTokenError
import jwt

router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/signup/local",response_model=APIResponse[UserOut])
async def local_register(user_data:UserInForLocal,db:AsyncSession = Depends(get_db)):
  user_data_for_db = UserInForDb(**user_data.model_dump(exclude={"password"}),hashed_password=hash_password(user_data.password))
  try:
    user = await register_local_user(user_data=user_data_for_db, db=db)
  except EmailAlreadyExistsError:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already exist!!!")
  user_out = UserOut.model_validate(user)
  return success_response(status_code=status.HTTP_201_CREATED,message="user succssfully sign up!!!",data=user_out.model_dump(mode="json"))


@router.post("/login/social",response_model=APIResponse[TokenResponse])
async def third_party_login(user_data:ThirdPartyLogin,db:AsyncSession = Depends(get_db)):

  user = await login_with_third_party(user_data=user_data,db=db)
  data = {
  "sub":str(user.id),
  "is_premium":user.is_premium,
  "type":"access"
  }
  access_token = token_generator(data=data,expire=timedelta(hours=1),encryption_key=settings.ACCESS_KEY)
  refresh_token = token_generator(data={"sub":str(user.id)},expire=timedelta(days=7),encryption_key=settings.REFRESH_KEY)
  response =  success_response(status_code=200,message="successfully login",data=TokenResponse(access_token=access_token,type="access").model_dump())
  response.set_cookie(
    key="refresh_token",
    value=refresh_token,
    httponly=True,
    secure=False,
    max_age=3600*24*7
  )

  return response


@router.post("/login/local",response_model=APIResponse[TokenResponse])
async def local_login(user_data:OAuth2PasswordRequestForm = Depends(),db:AsyncSession = Depends(get_db)):#it accept user data as a form data not as a json type
  try:
    user = await authenticate_local_user(user_data=LocalLogin(email=user_data.username,password=user_data.password),db=db)
    data = {
    "sub":str(user.id),
    "is_premium":user.is_premium,
    "type":"access"
    }
    access_token = token_generator(data=data,expire=timedelta(hours=1),encryption_key=settings.ACCESS_KEY)
    refresh_token = token_generator(data={"sub":str(user.id)},expire=timedelta(days=7),encryption_key=settings.REFRESH_KEY)
    response =  success_response(status_code=200,message="successfully login",data=TokenResponse(access_token=access_token,type="access").model_dump())
    response.set_cookie(
      key="refresh_token",
      value=refresh_token,
      httponly=True,
      secure=False,
      max_age=3600*24*7
    )
  except InvalidCredentialsError:
    raise HTTPException(status_code=401,detail="Incorrect Email or Password!!!")
  return response


@router.post("/refresh")
async def refres_login(request:Request,db:AsyncSession = Depends(get_db)):
  refresh_token = request.cookies.get("refresh_token")
  try:
    payload = jwt.decode(refresh_token,settings.REFRESH_KEY,algorithms=[settings.ALGO])
    user_id = payload.get("sub")
    if not user_id:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="empty username.")
    user = await get_user_by_id(id=user_id,db=db)
    if not user:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="user doesn't exist.")
    data = {
    "sub":str(user.id),
    "is_premium":user.is_premium,
    "type":"access"
    }
    access_token = token_generator(data=data,expire=timedelta(hours=1),encryption_key=settings.ACCESS_KEY)
    refresh_token = token_generator(data={"sub":str(user.id)},expire=timedelta(days=7),encryption_key=settings.REFRESH_KEY)
    response =  success_response(status_code=200,message="login refreshed",data=TokenResponse(access_token=access_token,type="access").model_dump())
    response.set_cookie(
      key="refresh_token",
      value=refresh_token,
      httponly=True,
      secure=False,
      max_age=3600*24*7
    )
  except InvalidTokenError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")
    
  return response