from sqlalchemy import Column, String, Integer, DateTime
from utils.db import Base

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)

class OrderItemModel(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, nullable=False)
    item = Column(String, nullable=False)
    price = Column(String, nullable=False)