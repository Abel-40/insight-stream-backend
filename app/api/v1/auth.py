from fastapi import APIRouter,Depends,HTTPException,status
from app.services.auth_service import register_local_user,login_with_third_party,local_login
from app.schemas.user import UserInForLocal, UserOut,UserInForDb
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions.auth_exceptions import EmailAlreadyExistsError
from app.schemas.token import TokenResponse
from app.schemas.response import APIResponse
from app.core.security import hash_password
from app.dependencies.database import get_db
from app.utils.response import success_response
router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/local/login",response_model=APIResponse[UserOut])
async def local_register(user_data:UserInForLocal,db:AsyncSession = Depends(get_db)):
  user_data_for_db = UserInForDb(**user_data.model_dump(exclude={"password"}),hashed_password=hash_password(user_data.password))
  try:
    user = await register_local_user(user_data=user_data_for_db, db=db)
  except EmailAlreadyExistsError:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already exist!!!")
  user_out = UserOut.model_validate(user)
  return success_response(status_code=status.HTTP_201_CREATED,message="user succssfully sign up!!!",data=user_out.model_dump(mode="json"))