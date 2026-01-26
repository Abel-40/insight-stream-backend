from core.db import AsyncLocalSession

async def get_db():
  with AsyncLocalSession as session:
    yield session
  