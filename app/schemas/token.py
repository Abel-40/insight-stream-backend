from pydantic import BaseModel

class TokenResponse(BaseModel):
  access_token:str
  type:str