from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,or_
from app.models.topic import Topic
from app.exceptions.topic_exceptions import TopicAlreadyExistError,TopicDoesNotExist
from uuid import UUID
async def create_topic(db:AsyncSession,name:str):
  existing_topic = (await db.scalars(select(Topic).where(Topic.name == name))).one_or_none()
  if existing_topic:
    raise TopicAlreadyExistError
  
  topic = Topic(name=name)
  db.add(topic)
  await db.commit()
  
  return topic
async def list_active_topics(page:int,page_size:int,db:AsyncSession) :
  count_query = select(func.count(Topic.id)).where(Topic.is_active == True)
  total_topics = await db.scalar(count_query) or 0
  data_query = select(Topic).where(Topic.is_active == True).offset((page - 1) * page_size).limit(page_size)
  topics = await db.scalars(data_query)
  
  return total_topics, topics.all()



async def get_topic_by_id_or_name(
    db: AsyncSession, 
    id: UUID | None = None, 
    name: str | None = None
) -> Topic:
    query = select(Topic)
    if id and name:
        query = query.where(or_(Topic.id == id, Topic.name == name))
    elif id:
        query = query.where(Topic.id == id)
    elif name:
        query = query.where(Topic.name == name)
    else:
        raise ValueError("Either id or name must be provided")

    result = await db.execute(query)
    topic = result.scalar_one_or_none()

    if not topic:
        raise TopicDoesNotExist()
        
    return topic
  
    
    