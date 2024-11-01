from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String, nullable=True)
    queries_today = Column(Integer, default=0)
    last_query_reset = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer)
    message_id = Column(Integer)
    content = Column(String)
    created_at = Column(DateTime, server_default=func.now()) 