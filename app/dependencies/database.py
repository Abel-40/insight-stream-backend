from app.core.db import AsyncLocalSession
from sqlalchemy.ext.asyncio import AsyncSession
async def get_db():
  async with AsyncLocalSession() as session:
    yield session
  