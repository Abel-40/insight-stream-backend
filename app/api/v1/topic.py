from fastapi import APIRouter,Depends,Body,HTTPException,status
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.topic import Topic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated,List
from app.services.topic_service import create_topic,list_active_topics,get_topic_by_id_or_name
from app.exceptions.topic_exceptions import TopicAlreadyExistError
from app.schemas.response import APIResponse,PaginatedResponse
from app.utils.response import success_response
from app.utils.pagination import paginate
from app.schemas.topic import TopicSchema,TopicCreate,TopicUpdate
from app.exceptions.topic_exceptions import TopicDoesNotExist
from uuid import UUID
router = APIRouter(prefix="/topic",tags=["topic"])

@router.post("/create",response_model=APIResponse[TopicSchema])
async def create_topic_endpoint(topic_data:TopicCreate,current_user:User = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
  try:
    topic = await create_topic(name=topic_data.name,db=db)
  except TopicAlreadyExistError:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="topic already exist!!!")
  topic_for_response = TopicSchema.model_validate(topic)
  return success_response(
    status_code=status.HTTP_201_CREATED,
    message="topic created successfully!!!",
    data=topic_for_response.model_dump(mode="json")
  )
  
@router.get("/",response_model = APIResponse[PaginatedResponse[List[TopicSchema]]])
async def get_topics_endpoint(page:int=1,page_size:int=10,current_user:User = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
  total, active_topics = await list_active_topics(page=page,page_size=page_size,db=db)
  topic_for_response = [TopicSchema.model_validate(topic).model_dump(mode="json") for topic in active_topics]
  pagination = paginate(items=topic_for_response,total=total,page=page,item_size=page_size)
  print(pagination)
  return success_response(status_code=status.HTTP_200_OK,message="topics fetched successfully!!!",data=pagination)

@router.get("/{id}",response_model=APIResponse[TopicSchema])
async def get_topic_by_id(id:UUID,current_user:User = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
  data_query = select(Topic).where(Topic.id == id)
  try:
    topic = await get_topic_by_id_or_name(id=id,db=db)
  except TopicDoesNotExist:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Topic doesn't exist!!!")
  return success_response(status_code=status.HTTP_200_OK,message="topic fetched!!",data=TopicSchema.model_validate(topic).model_dump(mode="json"))

@router.put("/{id}",response_model=APIResponse[TopicSchema])
async def update_topic(id:UUID,updated_content:TopicUpdate,current_user:User = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
  try:
    topic = await get_topic_by_id_or_name(id=id,db=db)
    for key,value in updated_content.model_dump(exclude_unset=True).items():
      setattr(topic,key,value)
    await db.commit()
    await db.refresh(topic)
  except TopicDoesNotExist:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Topic doesn't exist!!!")
  return success_response(status_code=status.HTTP_200_OK,message="Topic updated.",data=TopicSchema.model_validate(topic).model_dump(mode="json"))