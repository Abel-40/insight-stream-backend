from pydantic import BaseModel,ConfigDict,Field
from typing import Annotated
from datetime import datetime
from uuid import UUID


class TopicSchema(BaseModel):
  id:UUID
  name:Annotated[str,Field(max_length=255)]
  created_at:datetime
  model_config = ConfigDict(from_attributes=True)
class TopicCreate(BaseModel):
  name:Annotated[str,Field(max_length=255)]
  
class TopicUpdate(BaseModel):
  name:Annotated[str | None,Field(max_length=255)] = None
  is_active:bool | None = None