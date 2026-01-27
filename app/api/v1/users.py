from fastapi import APIRouter

router = APIRouter(prefix="/user",tags=["user"])

@router.get("/profile")
async def profile():
  return {"username":"Abel"}