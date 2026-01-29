from pydantic import BaseModel,EmailStr,Field,ConfigDict
from typing import Annotated,Optional
from uuid import UUID
from datetime import datetime
class User(BaseModel):
  email:EmailStr
  full_name:Annotated[Optional[str],Field(max_length=255)] = None
  
class UserInForLocal(User):
  password:Annotated[str,Field(min_length=8)]

class UserInForDb(User):
  hashed_password:Annotated[str,Field(max_length=255)]
  
class UserOut(BaseModel):
  id:UUID
  email:EmailStr
  full_name:Annotated[str,Field(max_length=255)]
  is_premium:bool
  created_at:datetime
  model_config = ConfigDict(from_attributes=True)

class LocalLogin(BaseModel):
  email:EmailStr
  password:str
  
class ThirdPartyLogin(BaseModel):
  provider:str
  email:EmailStr
  provider_account_id:str