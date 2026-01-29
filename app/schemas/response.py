from pydantic import BaseModel
from typing import TypeVar,Generic,Any,Dict,List

T = TypeVar("T")
class APIResponse(BaseModel,Generic[T]):
  success:bool
  message:str
  data:T | None = None
  errors:str | Dict[str,Any] | None = None
  meta: Dict[str,Any] | None = None
  
class PaginationMeta(BaseModel):
  page:int
  item_size:int
  total_items:int
  total_pages:int

I = TypeVar("I")
class PaginatedResponse(BaseModel, Generic[I]):
  items:List[I]
  meta:PaginationMeta
  