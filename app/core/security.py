from pwdlib import PasswordHash
from datetime import datetime,timedelta
from app.core.config import settings
import jwt

password_hash = PasswordHash.recommended()
def hash_password(password:str):
  return password_hash.hash(password=password)

def verify_password(entered_password:str,password_in_db:str):
  return password_hash.verify(entered_password,password_in_db)

def token_generator(data,expire:timedelta,encryption_key):
  to_encode = data.copy()
  expire = datetime.now() + expire
  to_encode.update({"exp":expire})
  token = jwt.encode(to_encode,encryption_key,settings.ALGO)
  return token