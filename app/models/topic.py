from sqlalchemy.orm import mapped_column, Mapped,relationship
from sqlalchemy import select, Integer, String, DateTime,ForeignKey,func,Table,Column
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base
from typing import List


user_topics = Table(
  "user_topics",
  Base.metadata,
  Column("user_id",UUID(as_uuid=True),ForeignKey("users.id"),primary_key=True),
  Column("topic_id",UUID(as_uuid=True),ForeignKey("topics.id"),primary_key=True),
  Column("topic_selected_date",DateTime(timezone=True), server_default=func.now())
)

class Topic(Base):
  __tablename__ = "topics"
  
  id:Mapped[UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
  name:Mapped[str] = mapped_column(String(255),unique=True)
  created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
  
  users:Mapped[List["User"]] = relationship("User",secondary=user_topics,back_populates="topics")



  