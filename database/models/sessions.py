from sqlalchemy import Column, Integer, String, DateTime

from utils.db import Base

class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(String, unique=True, nullable=True)
    user_id = Column(Integer, nullable=False, index=True)
    created = Column(DateTime, nullable=False)
    user_agent = Column(String, nullable=False)

