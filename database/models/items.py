from sqlalchemy import Column, Integer, String, Float
from utils.db import Base

class ItemModel(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)
    desc = Column(String)
    img = Column(String)
