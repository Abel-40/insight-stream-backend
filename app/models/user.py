from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import String,Integer,DateTime,Boolean,func,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import List
import uuid

Base = declarative_base()

class AuthAccount(Base):
  __tablename__="auth_accounts"
  id:Mapped[UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
  provider:Mapped[str] = mapped_column(String(65),nullable=False)
  provider_account_id:Mapped[str] = mapped_column(String(255),nullable=False,unique=True)
  user_id:Mapped[UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
  created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
  
  user:Mapped["User"] = relationship("User",back_populates="auth_accounts")

class User(Base):
  __tablename__="users"
  
  id:Mapped[UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
  email:Mapped[str] = mapped_column(String(255),unique=True,nullable=False)
  full_name:Mapped[str] = mapped_column(String(255),nullable=True)
  hashed_password:Mapped[str] = mapped_column(String(255),nullable=True)
  is_premium:Mapped[bool] = mapped_column(Boolean,default=False)
  created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
  
  auth_accounts:Mapped[List[AuthAccount]] = relationship("AuthAccount",back_populates="user",passive_deletes=True)
  


