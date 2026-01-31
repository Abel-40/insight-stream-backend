from typing import List,Any
from math import ceil
def paginate(
  items:List[Any],
  total:int,
  page:int,
  item_size:int
):
  return {
    "items":items,
    "meta":{
      "page":page,
      "item_size":item_size,
      "total_items":total,
      "total_pages":ceil(total/item_size)
    }
  }