from pydantic_settings import BaseSettings
from pathlib import Path

BASE_URL = Path(__file__).resolve().parents[2] #parents[0] is the config folder
class Settings(BaseSettings):
  DB_URL:str
  ACCESS_KEY:str
  REFRESH_KEY:str
  class Config:
    env_file = BASE_URL/".env"
    

settings = Settings()