from fastapi import FastAPI
from .api.v1 import users

app = FastAPI()
app.include_router(users.router)
@app.get("/check")
async def check():
  return {"msg":"it works"}